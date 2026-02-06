from __future__ import annotations
from orb_models.forcefield import pretrained
from orb_models.forcefield.calculator import ORBCalculator


def build_orb_calculator(cfg: dict):
    """
    ORB calculator.
    """

    calculator_cfg = cfg["calculator"]
    model_name = calculator_cfg["model"]
    model_parameters = calculator_cfg.get("model_parameters", {})
    wrapper_parameters = calculator_cfg.get("wrapper_parameters", {})

    if model_parameters is None:
        model_parameters = {}

    if wrapper_parameters is None:
        wrapper_parameters = {}

    if model_name == "pretrained.orb_v3_conservative_omol":
        orbff = pretrained.orb_v3_conservative_omol(**model_parameters)
    else:
        raise ValueError(f"Unknown ORB model in config: {model_name}")

    calculator = ORBCalculator(
        orbff,
        **wrapper_parameters
    )

    return calculator
