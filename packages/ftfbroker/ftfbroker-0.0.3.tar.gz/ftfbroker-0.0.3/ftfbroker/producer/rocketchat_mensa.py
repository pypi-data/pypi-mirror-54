import logging
from typing import Iterable, Tuple

from ftfbroker.producer.general_producer import GeneralProducer
from ftfbroker.protobuf.ftf.rocketchat_mensa_pb2 import (
    Option, RocketchatMensa, RocketchatMensaV1
)

logger = logging.getLogger(__name__)


def _create_envelop(options: Iterable[Tuple[str, Iterable[str]]]) -> RocketchatMensa:
    payload = RocketchatMensaV1()

    opts = [Option(time=t, users=u) for t, u in options]
    payload.options.extend(opts)

    return RocketchatMensa(payload_v1=payload)


class RocketchatMensaProducer(GeneralProducer):
    def sendV1(self, options: Iterable[Tuple[str, Iterable[str]]]) -> None:
        """
        Expect options in the form:

        [
            ('11:30', ['Person A', 'Person B']),
            ('12:00', ['Person C'])
        ]

        """
        super().send(_create_envelop(options))

    @classmethod
    def sendV1_(cls, options: Iterable[Tuple[str, Iterable[str]]]) -> None:
        cls.instance().send(_create_envelop(options))
