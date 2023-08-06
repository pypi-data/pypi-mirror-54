
from google.protobuf.message import Message as ProtobufMessage

from ftfbroker.protobuf.ftf.automate_stock_pb2 import AutomateStock
from ftfbroker.protobuf.ftf.rocketchat_mensa_pb2 import RocketchatMensa

# Available topics
TOPIC_AUTOMATE_STOCK = 'ftf_automate_stock'
TOPIC_ROCKETCHAT_MENSA = 'ftf_rocketchat_stock'

TOPIC_TO_PROTO = {
    TOPIC_AUTOMATE_STOCK: AutomateStock,
    TOPIC_ROCKETCHAT_MENSA: RocketchatMensa,
}

PROTO_TO_TOPIC = {v.__name__: k for k, v in TOPIC_TO_PROTO.items()}


def get_topic_from_protobuf(protobuf: ProtobufMessage) -> str:
    return PROTO_TO_TOPIC[protobuf.__class__.__name__]
