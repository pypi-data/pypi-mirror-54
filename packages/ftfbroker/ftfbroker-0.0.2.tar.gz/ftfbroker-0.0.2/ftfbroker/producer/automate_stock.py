import logging

from ftfbroker.producer.general_producer import GeneralProducer
from ftfbroker.protobuf.ftf.automate_stock_pb2 import (
    AutomateStock, AutomateStockV1
)

logger = logging.getLogger(__name__)


class AutomateStockProducer(GeneralProducer):
    def sendV1(self, dms_id: str, payload: AutomateStockV1) -> None:
        protobuf = AutomateStock(payload_v1=payload)

        super().send(protobuf, key=dms_id)

    @classmethod
    def sendV1_(cls, dms_id: str, payload: AutomateStockV1) -> None:
        protobuf = AutomateStock(payload_v1=payload)

        cls.instance().send(protobuf, key=dms_id)
