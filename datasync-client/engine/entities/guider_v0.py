import os
import json
from engine.entities.base import BaseEntity
from engine.entities.origins.origin_factory import OriginFactory
from engine.entities.origins.origin_base import OriginBase
from engine.entities.destination import Destination
from engine.entities.rules import Rules
import pprint
from typing import Dict, Any


class Guider(BaseEntity):
    name: str
    data: dict
    origin_root: str
    originsList: list[OriginBase]
    destinations: Destination
    rules: Rules
    dictionaries: Any
    dataframe: Any
    dataframe_structured: Any

    def __init__(self, name: str, data: dict):
        self.name = name
        self.data = data
        self.origin_root = data["origin_root"]
        self.originsList = OriginFactory(data.get("origin", {}))
        self.destinations = Destination(data["destination"])
        self.rules = Rules(data["mapping"])
        self.dictionaries = {}
        self.buildData()
        # pprint.pprint(json.dumps(self.dataframe, indent=2))
        # with open("resultado.json", "w", encoding="utf-8") as f:
        #     json.dump(self.dataframe, f, ensure_ascii=False, indent=4)
        # print(" =========== " * 10)
        # quit()
    
    def buildData(self):
        self.dataframe = {}
        self.dataframe_structured = {}
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

        for origin in self.originsList:
            self.dictionaries[origin["name"]] = origin["data"]

        self.dataframe = self.getCurrentDataframe(
            origin_root_data,
            self.origin_root,
            origin_root_data["primary_key"],
            True,
        )

    def getCurrentDataframe(
        self, origin: OriginBase, name: str, group_by: str, root: bool
    ) -> object:
        if name not in self.dataframe_structured:
            self.dataframe_structured[name] = {}

        if group_by not in self.dataframe_structured[name]:
            self.dataframe_structured[name][group_by] = {}

        childs = origin["relation"]["childs"]
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

            child["data"] = self.getCurrentDataframe(
                child_data, child["name"], child["foreign_key"], False
            )

        current_dataframe = {}
        for index, row in origin["data"].iterrows():
            if row[group_by] not in current_dataframe:
                current_dataframe[row[group_by]] = {}
            current_record = row.to_dict()

            if childs:
                for child in childs:
                    try:
                        if current_record[child["foreign_key"]] in child["data"]:
                            current_record[child["name"]] = child["data"][
                                current_record[child["foreign_key"]]
                            ]
                    except Exception as e:
                        print(f"Error getting child {child['name']}: {e}")
                        print(f"current_record: {current_record}")
                        print(type(current_record))
                        print(f"Child: {child}")
                        print(f"Row: {row}")
                        print(f"Child foreign key: {child['foreign_key']}")
                        print(
                            f"Child foreign key in current_record: {child['foreign_key'] in current_record}"
                        )
                        print(
                            f"Child foreign key value: [ {current_record[child['foreign_key']]} ]"
                        )
                        print(f"Child data: {child['data']}")
                        print(" =*** " * 10)
                        quit()

            try:
                new_index = (
                    index if not origin["primary_key"] else row[origin["primary_key"]]
                )
                if root:
                    current_dataframe[new_index] = current_record
                else:
                    current_dataframe[row[group_by]][new_index] = current_record
            except Exception as e:
                print(f"Error getting new index: {e}")
                print(f"Row: {row}")
                print(f"Origin: {origin}")
                print(" =*** " * 10)
                quit()

        return current_dataframe


def create_guider(name: str) -> Guider:
    try:
        full_path = os.path.join(
            os.path.abspath(os.path.join("guiders")), f"{name}.json"
        )
        if not os.path.exists(full_path):
            raise ValueError(f"Guider {name} not found")
        if not os.path.isfile(full_path):
            raise ValueError(f"Guider {name} is not a valid JSON file")
        with open(full_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        return Guider(name, data)
    except FileNotFoundError:
        raise ValueError(f"Guider {name} not found")
    except json.JSONDecodeError:
        raise ValueError(f"Guider {name} is not a valid JSON file")
    except Exception as e:
        raise ValueError(f"Error creating guider object {name}: {e}")
