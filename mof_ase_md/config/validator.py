from __future__ import annotations

class ConfigError(ValueError):
    pass


def _require(cfg: dict, path: str):
    cur = cfg
    for key in path.split("."):
        if not isinstance(cur, dict) or key not in cur:
            raise ConfigError(f"Missing required config key: {path}")
        cur = cur[key]
    return cur


def _require_str(cfg: dict, path: str) -> str:
    val = _require(cfg, path)
    if not isinstance(val, str) or not val.strip():
        raise ConfigError(f"{path} must be a non-empty string")
    return val


def _require_bool(cfg: dict, path: str) -> bool:
    val = _require(cfg, path)
    if not isinstance(val, bool):
        raise ConfigError(f"{path} must be a boolean (true/false)")
    return val


def _require_int_gt(cfg: dict, path: str, min_value: int) -> int:
    val = _require(cfg, path)
    if not isinstance(val, int) or val <= min_value:
        raise ConfigError(f"{path} must be an int > {min_value}")
    return val


def _require_num_gt(cfg: dict, path: str, min_value: float) -> float:
    val = _require(cfg, path)
    if not isinstance(val, (int, float)) or val <= min_value:
        raise ConfigError(f"{path} must be a number > {min_value}")
    return float(val)


def _require_num(cfg: dict, path: str) -> float:
    val = _require(cfg, path)
    if not isinstance(val, (int, float)):
        raise ConfigError(f"{path} must be a number")
    return float(val)


def validate_config(cfg: dict) -> dict:
    # system
    _require_str(cfg, "system.input_file")
    _require_bool(cfg, "system.pbc")

    # calculator (force field choice)
    _require_str(cfg, "calculator.name")
    _require_str(cfg, "calculator.model")

    params = cfg.get("calculator", {}).get("parameters", {})
    if params is None:
        params = {}
        cfg["calculator"]["parameters"] = params
    if not isinstance(params, dict):
        raise ConfigError("calculator.parameters must be a dict")

    # md
    ensemble = _require_str(cfg, "md.ensemble").lower()
    if ensemble not in ("nve", "nvt", "npt"):
        raise ConfigError("md.ensemble must be one of: nve, nvt, npt")
    cfg["md"]["ensemble"] = ensemble  # normalize

    total_steps = _require_int_gt(cfg, "md.total_steps", 0)
    timestep_fs = _require_num_gt(cfg, "md.timestep_fs", 0.0)

    # state
    if ensemble in ("nvt", "npt"):
        _require_num_gt(cfg, "state.temperature_K", 0.0)

    if ensemble == "npt":
        _require_num(cfg, "state.pressure_bar")

    # output
    _require_str(cfg, "output.workdir")
    _require_str(cfg, "output.trajectory_file")
    _require_str(cfg, "output.log_file")

    traj_interval = _require_int_gt(cfg, "output.traj_interval", 0)
    log_interval = _require_int_gt(cfg, "output.log_interval", 0)

    # consistency
    if traj_interval > total_steps:
        raise ConfigError("output.traj_interval cannot be greater than md.total_steps")
    if log_interval > total_steps:
        raise ConfigError("output.log_interval cannot be greater than md.total_steps")

    return cfg
