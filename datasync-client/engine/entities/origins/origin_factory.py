from engine.entities.origins.file.local.origin_file_local_csv import OriginFileLocalCSV
from engine.entities.origins.origin_base import OriginBase
from engine.entities.origins.request.origin_request_json import OriginRequestJson
from engine.tools.logger import LogLevel, log


def OriginFactory(originsGuider: dict, json_data: dict = None) -> list[OriginBase]:
    origins = []
    for originKey in originsGuider.keys():
        current_origin = originsGuider[originKey]

        new_origin = None
        match current_origin.get("type", None):
            case "file":
                new_origin = OriginFileFactory(current_origin)
            case "request":
                new_origin = OriginRequestJsonFactory(current_origin, json_data)
            case _:
                raise ValueError(f"Invalid origin type: {current_origin['type']}")

        if new_origin:
            origins.append(
                {
                    "name": new_origin.origins["name"],
                    "primary_key": new_origin.origins["primary_key"],
                    "relation": new_origin.origins["relation"],
                    "data": new_origin.data,
                }
            )
    return origins


def OriginRequestFactory(origin: dict, json_data: dict) -> OriginBase | None:
    print("OriginRequestFactory")
    match origin.get("meta", {}).get("type", None):
        case "json":
            return OriginRequestJsonFactory(origin, json_data)
        case _:
            raise ValueError(f"Invalid origin meta.type: {origin['meta']['type']}")


def OriginRequestJsonFactory(origin: dict, json_data: dict) -> OriginBase | None:
    print("OriginRequestJsonFactory")
    return OriginRequestJson(origin, json_data)


def OriginFileFactory(origin: dict) -> OriginBase | None:
    match origin.get("meta", {}).get("storage", None):
        case "local":
            return OriginFileLocalFactory(origin)
        case "aws_s3":
            not_implemented(origin)
            return None
        case _:
            raise ValueError(f"Invalid origin meta.type: {origin['meta']['type']}")


def OriginFileLocalFactory(origin: dict) -> OriginFileLocalCSV | None:
    match origin.get("meta", {}).get("type", None):
        case "csv":
            return OriginFileLocalCSV(origin)
        case "xlsx":
            not_implemented(origin)
            return None
        case _:
            raise ValueError(f"Invalid origin meta.type: {origin['meta']['type']}")


def not_implemented(origin: dict) -> None:
    log(
        f"Origin '{origin['type']}.{origin['meta']['type']}.{origin['meta']['storage']}' is not implemented",
        LogLevel.ERROR,
    )
