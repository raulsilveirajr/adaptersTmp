import json
import requests
import uuid

from engine.entities.destination import Destination
from engine.entities.guider import Guider
from engine.tools.logger import LogLevel, log


def sender_guider(
    guider: Guider,
    current_destination: Destination,
    destination_name: str,
    payload: dict,
    origin_data: dict,
) -> dict:
    # TODO: validar se é para enviar um payload encapsulado (padrão para o nosso backend) ou não (payload direto para outro destino)
    payload = get_encapsulated_payload(
        payload,
        current_destination,
        destination_name,
        origin_data,
    )
    log(f"Guider name: {guider.name}", LogLevel.DEBUG)
    log(f"Sending {guider.name} guider", LogLevel.DEBUG)

    log(f"Destinations: {current_destination['url']}", LogLevel.DEBUG)
    url = current_destination["url"]
    log(f"URL: {url}", LogLevel.DEBUG)
    headers = current_destination["headers"]
    log(f"Headers: {headers}", LogLevel.DEBUG)
    log(
        f"Payload: {json.dumps(payload, indent=2, ensure_ascii=False)}",
        LogLevel.DEBUG,
    )
    print(" =============================== " * 5)
    try:
        response = requests.post(url, json=payload, headers=headers)
        log(f"Response: {response.status_code}", LogLevel.INFO)
        log(f"Response: {response.text}", LogLevel.DEBUG)
    except Exception as e:
        log(f"Error sending {guider.name} guider: {e}", LogLevel.ERROR)
    return {"name": guider.name}


def get_encapsulated_payload(
    payload: dict,
    current_destination: Destination,
    destination_name: str,
    origin_data: dict,
) -> dict:
    # print(" =============================== " * 5)
    # print("origin_data:")
    # print(origin_data)
    # print(type(origin_data))

    json_str = dict()
    for index, value in origin_data.items():
        json_str[index] = '"' + str(value) + '"'

    # print(json_str)
    # print("  ")


    # # Converta a Series para um objeto JSON
    # json_str = origin_data.to_json()

    # # Carregue a string JSON em um objeto Python
    # json_obj = json.loads(json_str)

    # # Converta o objeto Python de volta para uma string JSON com aspas duplas
    # json_str_with_double_quotes = json.dumps(json_obj)

    # print(json_str_with_double_quotes)

    # quit()


    return {
        "traceid": current_destination["topic"] + "_" + str(uuid.uuid4()),
        "vendor": "PIL",
        "topic": current_destination["topic"],
        "marketplace": destination_name,
        "marketplace_meta": current_destination["marketplace_meta"],
        "payload": payload,
        "origin_data": json_str,
    }


