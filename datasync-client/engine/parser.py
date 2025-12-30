import json
import math
import pprint
import re

from engine.entities.guider import Guider

# from engine.entities.destination import Destination
from engine.entities.origins.origin_base import OriginBase
from engine.sender import sender_guider
from engine.tools.logger import LogLevel, log


def parser_guider(guider: Guider) -> None:
    for destination_name in guider.destinationsList.destinationsList.keys():
        current_destination = guider.destinationsList.destinationsList[destination_name]
        log(f"Processing Destination: {destination_name}")

        match current_destination["body_type"]:
            case "object":
                parse_guider_object(guider, current_destination, destination_name)
            case "list":
                parse_guider_list(guider, current_destination, destination_name)
            case _:
                log(
                    f"Invalid body type: {guider.destinations.destination['body_type']}",
                    LogLevel.ERROR,
                )


def parse_guider_object(
    guider: Guider, current_destination: dict, destination_name: str
) -> None:
    guider_name: str = guider.name
    originsList: list[OriginBase] = guider.originsList

    log(f"Parsing {guider_name} guider")
    main_origin = next(
        (origin for origin in originsList if origin["name"] == guider.origin_root),
        None,
    )

    total_rows = main_origin["data"].shape[0]
    for index, current_line in main_origin["data"].iterrows():
        # TODO: Implementar a lógica de pre-routine
        payload = get_origin_value_object(
            current_line,
            current_destination["mapping"],
        )
        if total_rows < 20 or index % 1000 == 0 or index == total_rows - 1:
            # print(f"payload: {json.dumps(payload, indent=2)}")
            # print(payload)
            print(f"index: {index}/{total_rows}")
            sender_guider(
                guider,
                current_destination,
                destination_name,
                payload,
                current_line,
            )
        # TODO: Implementar a lógica de pos-routine

    return {"name": guider_name}


def get_origin_value_object(current_line, mapping, level=0):
    payload = {}
    for rule in mapping:
        try:
            attributeName = rule["name"]
        except KeyError:
            print(f"Invalid rule: {rule}", LogLevel.ERROR)
            continue

        match rule["datatype"]:
            case "string":
                try:
                    value = get_origin_value(current_line, rule)
                    if (
                        (isinstance(value, str) and (not value or value == "nan"))
                        or (isinstance(value, (int, float)) and (math.isnan(value)))
                        or (value is None)
                    ):
                        value = ""

                    payload[attributeName] = '"' + value.strip() + '"'
                except Exception as e:
                    log(
                        f" >> Error getting origin value (type 'string'): {e} - {attributeName}"
                    )
                    quit()
                    payload[attributeName] = None
            case "number":
                payload[attributeName] = '"' + str(get_origin_value(current_line, rule)) + '"'
            case "date":
                log("Datatype date not implemented yet", LogLevel.ERROR)
            case "boolean":
                payload[attributeName] = '"' + str(rule["origin"]["meta"]["value"]) + '"'
            case "expression":
                try:
                    payload[attributeName] = get_origin_value_expression(
                        current_line, rule
                    )
                except Exception as e:
                    log(
                        f" >> Error getting origin value (type 'expression'): {e} - {attributeName}"
                    )
                    payload[attributeName] = None
            case "object":
                payload[attributeName] = get_origin_value_object(
                    current_line, rule["mapping"], level + 1
                )
            case "list":
                # log("Datatype list not implemented yet", LogLevel.ERROR)
                continue
            case _:
                log(f"Invalid datatype: {rule['datatype']}", LogLevel.ERROR)

        # log(
        #     f"Payload get_origin_value_object : {json.dumps(payload, indent=2)}",
        #     LogLevel.DEBUG,
        # )

    return payload


def parse_guider_list(guider_name, origins, destination, rules):
    pass


def get_origin_value(current_line, rule):
    try:
        key = rule["origin"]["meta"]["column"]
        value = current_line[key]
        return value
    except KeyError:
        return f"ERROR getting origin value: {rule["origin"]["meta"]["column"]} from {current_line.to_dict()}"
    return None


def get_origin_value_expression(current_line, rule):
    expression = rule["origin"]["meta"]["expression"]
    if "<<" in expression:
        field_names = re.findall(r"<<(\w+)>>", expression)
        for field in field_names:
            value = current_line[field]
            if not isinstance(value, str):
                value = str(value)
            expression = expression.replace(f"<<{field}>>", value)

    value = eval(expression)

    return '"' + str(value) + '"'


def get_conversion_from_list(
    list: dict, value: str, default_key: str, default_value: str
):
    if value not in list:
        if default_key not in list:
            return default_value
        return list[default_key]
    return list[value]
