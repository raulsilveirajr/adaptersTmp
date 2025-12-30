import json
import os
import pprint

from engine.entities.base import BaseEntity
from engine.entities.destination import Destination
from engine.entities.origins.origin_base import OriginBase
from engine.entities.origins.origin_factory import OriginFactory
from engine.entities.rules import Rules
from engine.tools.logger import log


class Guider(BaseEntity):
    def __init__(self, name: str, data: dict, jsonData: dict):
        self.name = name
        self.data = data
        self.jsonData = jsonData
        self.origin_root = data["origin_root"]
        self.originsList = OriginFactory(data.get("origin", {}), jsonData)
        self.destinationsList = Destination(data["destination"])
        self.dictionaries = {}
        self.buildData()
        # print(json.dumps(self.dataframe, ensure_ascii=False, indent=2))
        # with open("resultado.json", "w", encoding="utf-8") as f:
        #     json.dump(self.dataframe, f, ensure_ascii=False, indent=4)
        # print("===========" * 10)
        # quit()

    def buildData(self):
        # Criar o dicionário de dados de origem
        self.dataframe = {}
        self.dataframe_structured = {}

        # Obter os dados da origem principal
        origin_root_data = next(
            (
                origin
                for origin in self.originsList
                if origin["name"] == self.origin_root
            ),
            None,
        )
        if origin_root_data is None:
            raise ValueError(f"Main origin {self.origin_root} not found")

        # Preparar os dicionários com os dados de cada origem
        for origin in self.originsList:
            self.dictionaries[origin["name"]] = origin["data"]

        # Construir o DataFrame a partir da origem principal
        self.dataframe = self.getCurrentDataframe(
            origin_root_data,
            self.origin_root,
            origin_root_data["primary_key"],
            True,
        )

    def getCurrentDataframe(
        self, origin: OriginBase, name: str, group_by: str, root: bool
    ) -> dict:
        if name not in self.dataframe_structured:
            self.dataframe_structured[name] = {}

        if group_by not in self.dataframe_structured[name]:
            self.dataframe_structured[name][group_by] = {}

        # Obter as relações de filhos
        childs = origin["relation"]["childs"]

        # Processar cada filho recursivamente
        for child in childs:
            child_data = next(
                (
                    origin
                    for origin in self.originsList
                    if origin["name"] == child["name"]
                ),
                None,
            )

            if child_data is None:
                raise ValueError(f"Child origin {child['name']} not found")

            # Recurso recursivo para construir o DataFrame dos filhos
            child["data"] = self.getCurrentDataframe(
                child_data, child["name"], child["foreign_key"], False
            )

        # Criar o DataFrame atual com os dados aninhados
        current_dataframe = {}
        for index, row in origin["data"].iterrows():
            if row[group_by] not in current_dataframe:
                current_dataframe[row[group_by]] = {}
            current_record = row.to_dict()

            # Adicionar dados dos filhos
            if childs:
                for child in childs:
                    try:
                        if current_record[child["foreign_key"]] in child["data"]:
                            current_record[child["name"]] = child["data"][
                                current_record[child["foreign_key"]]
                            ]
                    except KeyError as e:
                        print(f"Error processing child {child['name']}: {e}")
                        continue

            # Inserir no DataFrame final
            new_index = (
                index if not origin["primary_key"] else row[origin["primary_key"]]
            )
            if root:
                current_dataframe[new_index] = current_record
            else:
                current_dataframe[row[group_by]][new_index] = current_record

        return current_dataframe


def create_guider(name: str, jsonData: dict = {}) -> Guider:
    log(f"Creating guider (create_guider) {name}")
    full_path = os.path.join(os.path.abspath(os.path.join("guiders")), f"{name}.json")
    if not os.path.exists(full_path):
        raise ValueError(f"create_guider - Guider {name} not found")
    if not os.path.isfile(full_path):
        raise ValueError(f"create_guider - Guider {name} is not a valid JSON file")
    try:
        with open(full_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        return Guider(name, data, jsonData)
    except FileNotFoundError:
        raise ValueError(f"create_guider - Guider {name} not found")
    except json.JSONDecodeError:
        raise ValueError(f"create_guider - Guider {name} is not a valid JSON file")
    except Exception as e:
        raise ValueError(f"create_guider - Error creating guider object {name}: {e}")
