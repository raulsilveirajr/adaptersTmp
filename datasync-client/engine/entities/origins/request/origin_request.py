from engine.entities.origins.origin_base import OriginBase


class OriginRequest(OriginBase):
    def __init__(self, origin: dict):
        super().__init__(origin)
