from engine.entities.origins.origin_base import OriginBase


class OriginFileLocal(OriginBase):
    def __init__(self, origin: dict):
        super().__init__(origin)
