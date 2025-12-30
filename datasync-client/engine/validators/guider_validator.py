import os


def validate_guider(guider: str) -> bool:
    full_path = os.path.join(os.path.abspath(os.path.join("guiders")), f"{guider}.json")
    print(os.path.exists(full_path))
    if not os.path.exists(full_path):
        raise ValueError("Guider not found")
    if not os.path.isfile(full_path):
        raise ValueError("Invalid guider")
    return validate_guider_json(guider)


def validate_guider_json(guider: str) -> bool:
    return True
