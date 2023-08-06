import datetime
import zlib
from typing import Any

import pytz
from google.protobuf.message import Message as ProtobufMessage

import ftfbroker.environment as env
from ftfbroker.protobuf.common.metaData_pb2 import MetaDataV1
from ftfbroker.topic import TOPIC_TO_PROTO


def load_message(topic: str, payload: bytes) -> Any:
    """Load a protobuf from string"""
    if topic in TOPIC_TO_PROTO:
        decomp = zlib.decompress(payload)
        protobuf = TOPIC_TO_PROTO[topic]()
        protobuf.ParseFromString(decomp)
        return protobuf
    raise ValueError(f'Unknown topic: {topic}')


def load_meta(protobuf: ProtobufMessage, message: Any) -> None:
    """ """
    meta = protobuf.WhichOneof('meta')
    if meta == 'meta_v1':
        meta_v1: MetaDataV1 = protobuf.meta_v1  # type: ignore
        meta_v1.offset = message.offset
        meta_v1.partition = message.partition
        return

    raise ValueError(f'Unknown meta data version: {meta}')


def serialize_message(protobuf: ProtobufMessage) -> bytes:
    """Serialize a protobuf object to string"""
    payload = protobuf.SerializeToString()
    return zlib.compress(payload, -1)


def add_meta(protobuf: Any) -> None:
    # if not hasattr(protobuf, 'meta'):
    #     raise ValueError('Protobuf has no meta field')

    protobuf.meta_v1.iso_date = datetime.datetime.now(pytz.utc).isoformat()
    protobuf.meta_v1.sending_service = env.KAFKA_SENDING_SERVICE
    protobuf.meta_v1.environment = MetaDataV1.Environment.Value(env.KAFKA_ENVIRONMENT)
