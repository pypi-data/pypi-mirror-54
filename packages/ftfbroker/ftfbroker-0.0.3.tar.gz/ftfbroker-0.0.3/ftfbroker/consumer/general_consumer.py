import json
import logging
import ssl
import threading
from time import sleep
from typing import Generator, List, Optional, Tuple

from google.protobuf.message import Message as ProtobufMessage
from kafka import KafkaConsumer
from tenacity import retry, stop_after_attempt, wait_exponential

import ftfbroker.environment as env
from ftfbroker import protoutils
from ftfbroker.exception import BrokerException

logger = logging.getLogger(__name__)


class GeneralConsumer:
    def __init__(
        self,
        enable_auto_commit: bool = True,
        group: Optional[str] = None,
        kafka_password: str = env.KAFKA_PASSWORD,
        kafka_server: str = env.KAFKA_SERVER,
        kafka_user: str = env.KAFKA_USER,
        ssl_context: ssl.SSLContext = env.DEFAULT_CONTEXT,
        start_point: str = 'latest',
        topic_pattern: Optional[str] = None,
        topics: Optional[List[str]] = None,
    ):

        if topics and topic_pattern:
            raise ValueError('Cannot specify topic(s) and topic_pattern.')
        self._commit_lock = threading.Lock()
        self.consumer: Optional[KafkaConsumer] = None
        self.enable_auto_commit = enable_auto_commit
        self.group = group
        self.kafka_password = kafka_password
        self.kafka_server = kafka_server
        self.kafka_user = kafka_user
        self.ssl_context = ssl_context
        self.start_point = start_point
        self.topic_pattern = topic_pattern
        self.topics = topics

        self.create_kafka_consumer()

    @retry(stop=stop_after_attempt(5), wait=wait_exponential(1))
    def create_kafka_consumer(self) -> None:
        """Try creating a Kafka Consumer"""
        try:
            self.consumer = KafkaConsumer(
                auto_offset_reset=self.start_point,
                bootstrap_servers=self.kafka_server,
                enable_auto_commit=self.enable_auto_commit,
                group_id=self.group,
                sasl_mechanism='PLAIN',
                sasl_plain_password=self.kafka_password,
                sasl_plain_username=self.kafka_user,
                security_protocol='SASL_SSL',
                ssl_context=self.ssl_context,
                key_deserializer=lambda x: None if x is None else x.decode('utf-8')
            )
            if self.topics:
                self.consumer.subscribe(topics=self.topics)
                logger.info(f'Consumer created for topics: {self.topics}')
            else:
                self.consumer.subscribe(pattern=self.topic_pattern)
                logger.info(f'Consumer created for topics: {self.topic_pattern}')
        except Exception as e:
            raise BrokerException('Error while creating a consumer') from e

    def consume(self) -> Generator[Tuple[Optional[str], ProtobufMessage], None, None]:
        if self.consumer is None:
            raise BrokerException('Cannot consume. Consumer is None')

        while True:
            try:
                for message in self.consumer:
                    try:
                        logger.debug(f"Message on {message.topic} received. Message: {message}")
                        try:
                            protobuf = protoutils.load_message(message.topic, message.value)
                            protoutils.load_meta(protobuf, message)
                            yield message.key, protobuf
                        except ValueError:
                            # Fallback: try to parse json
                            yield message.key, json.loads(message.value.decode('utf-8'))
                    except Exception as e:
                        raise BrokerException(
                            f'Consuming message from topic {message.topic} failed. Message: {message}') from e
            except BrokerException:
                # If something went wrong while parsing, do not try to recover
                # because something went wrong with protobuf
                try:
                    self.close()
                except Exception:
                    pass
                raise
            except Exception as e:
                # If it is something connection related, try to recover
                if self.consumer is None:
                    raise BrokerException("Consuming message failed. Consumer is None") from e
                else:
                    try:
                        self.close()
                    except Exception:
                        pass
                    self.consumer = None
                    self.create_kafka_consumer()
                    logger.error("Consuming message failed. Consumer recreated.", exc_info=True)
            finally:
                sleep(0.0001)

    def commit(self) -> None:
        """Commit the current offset manually"""
        try:
            with self._commit_lock:
                if self.consumer is None:
                    logger.warn('Could\'t commit. Consumer is None')
                else:
                    self.consumer.commit()
                    logger.debug('Committed successfully')
        except Exception as e:
            raise BrokerException('Couldn\'t commit') from e

    def close(self) -> None:
        """Close connection of consumer"""
        try:
            if self.consumer is None:
                logger.warn('Couldn\'t close consumer. Consumer is None')
            else:
                self.consumer.close()
        except Exception as e:
            raise BrokerException('Couldn\'t close consumer') from e
