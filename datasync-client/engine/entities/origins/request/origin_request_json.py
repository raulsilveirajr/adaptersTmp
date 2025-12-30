import pandas as pd

from engine.entities.origins.request.origin_request import OriginRequest


class OriginRequestJson(OriginRequest):
    def __init__(self, origin: dict, json_data: dict):
        super().__init__(origin)
        self.json_data = json_data
        self.loadOriginsData()

    def loadOriginsData(self):
        self.data = pd.DataFrame(self.json_data)
