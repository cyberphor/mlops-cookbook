# Standard library imports.
from typing import List

# Third party imports.
from yaml import safe_load


def get_experiment_plans(file_name) -> List:
    with open(file_name, mode="r", encoding="UTF-8") as file:
        experiment_plans = safe_load(file)
        if not isinstance(experiment_plans, list):
            raise ValueError(f"{file_name} is not a list of keys")
    return experiment_plans
