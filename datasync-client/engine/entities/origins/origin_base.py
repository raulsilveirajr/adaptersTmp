from engine.entities.base import BaseEntity


class OriginBase(BaseEntity):
    origins: dict
    primary_key: str
    data: dict

    def __init__(self, origin: dict):
        self.origins = origin
        self.primary_key = origin["primary_key"]
        self.data = []
