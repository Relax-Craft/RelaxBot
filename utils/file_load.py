import json


def application_questions() -> dict:
    with open(".\\utils\\questions.json", "r") as file:
        data = json.load(file)
    return data

def get_rules() -> dict:
    with open(".\\utils\\rules.json", "r") as file:
        data = json.load(file)
    return data