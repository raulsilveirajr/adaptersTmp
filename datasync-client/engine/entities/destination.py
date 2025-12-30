from engine.entities.base import BaseEntity


class Destination(BaseEntity):
    destinationsList: any

    def __init__(self, destinationsList: dict):
        self.destinationsList = destinationsList
