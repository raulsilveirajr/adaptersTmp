from engine.entities.guider import Guider, create_guider
from engine.parser import parser_guider
from engine.tools.logger import LogLevel, log


def exec_guider(guider_name: str, json_data: dict = None) -> None:
    log(f"Starting {guider_name} guider")
    try:
        guider = create_guider(guider_name, json_data)
        _process_guider(guider)
    except Exception as e:
        log(f"Error processing {guider_name} guider: {e}", LogLevel.ERROR)
    log(f"Finished {guider_name} guider")


def _process_guider(guider: Guider) -> None:
    log(f"Processing {guider.name} guider")
    parser_guider(guider)
