from __future__ import annotations

import logging
import ssl
from typing import Optional

from google.protobuf.message import Message as ProtobufMessage
from kafka import KafkaProducer

import ftfbroker.environment as env
from ftfbroker import protoutils, topic
from ftfbroker.exception import BrokerException

logger = logging.getLogger(__name__)


class GeneralProducer:
    _instance: Optional[GeneralProducer]

    def __init__(
        self,
        kafka_password: str = env.KAFKA_PASSWORD,
        kafka_server: str = env.KAFKA_SERVER,
        kafka_user: str = env.KAFKA_USER,
        ssl_context: ssl.SSLContext = env.DEFAULT_CONTEXT,
    ):
        self.kafka_password = kafka_password
        self.kafka_server = kafka_server
        self.kafka_user = kafka_user
        self.ssl_context = ssl_context

        self.producer = None
        self.create_kafka_producer()

    @classmethod
    def init_module(
        cls,
        kafka_password: str = env.KAFKA_PASSWORD,
        kafka_server: str = env.KAFKA_SERVER,
        kafka_user: str = env.KAFKA_USER,
        ssl_context: ssl.SSLContext = env.DEFAULT_CONTEXT,
    ) -> None:
        cls._instance = cls(
            kafka_password=kafka_password,
            kafka_server=kafka_server,
            kafka_user=kafka_user,
            ssl_context=ssl_context,
        )

    @classmethod
    def instance(cls) -> GeneralProducer:
        if cls._instance is None:
            raise BrokerException(f"Class instance not initialized. Call {cls.__name__}.init_module first")
        return cls._instance

    @classmethod
    def send_(cls, protobuf: ProtobufMessage, key: Optional[str] = None) -> None:
        cls.instance().send(protobuf, key=key)

    @classmethod
    def flush_(cls) -> None:
        cls.instance().flush()

    def create_kafka_producer(self) -> None:
        try:
            self.producer = KafkaProducer(
                bootstrap_servers=self.kafka_server,
                sasl_mechanism='PLAIN',
                sasl_plain_password=self.kafka_password,
                sasl_plain_username=self.kafka_user,
                security_protocol='SASL_SSL',
                ssl_context=self.ssl_context,
                key_serializer=lambda x: None if x is None else x.encode('utf-8'))
            logger.info(f"Producer created")
        except Exception as e:
            raise BrokerException('Error while creating a producer') from e

    def send(self, protobuf: ProtobufMessage, key: Optional[str] = None) -> None:
        if self.producer is None:
            raise BrokerException("Sending message failed. Producer is None")

        protoutils.add_meta(protobuf)
        value = protoutils.serialize_message(protobuf)
        top = topic.get_topic_from_protobuf(protobuf)

        logger.debug(f"Send message on {top}. Key: {key}, Message: {protobuf}")
        self.producer.send(top, value=value, key=key)

    def flush(self) -> None:
        if self.producer is None:
            raise BrokerException("Flushing failed. Producer is None")

        self.producer.flush()

    def close(self) -> None:
        """Close connection of producer"""
        try:
            if self.producer is None:
                logger.warn('Couldn\'t close producer. Producer is None')
            else:
                self.producer.close()
        except Exception as e:
            raise BrokerException('Couldn\'t close producer') from e
