from engine.entities.base import BaseEntity


class Rules(BaseEntity):
    rules: dict

    def __init__(self, rules: dict):
        self.rules = rules
