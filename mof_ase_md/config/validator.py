from __future__ import annotations
from mof_ase_md.md.methods import get_method_info


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

def _require_int(cfg: dict, path: str) -> int:
    val = _require(cfg, path)
    if not isinstance(val, int):
        raise ConfigError(f"{path} must be an int")
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

    # system: charge & spin (required for ML force fields like ORB)
    charge = _require_int(cfg, "system.charge")
    spin = _require_int(cfg, "system.spin")

    method = _require_str(cfg, "md.method").lower()
    cfg["md"]["method"] = method

    if spin <= 0:
        raise ConfigError("system.spin must be an int > 0")

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

    try:
        info = get_method_info(method)
    except Exception:
        raise ConfigError(f"Unknown md.method: {method}")

    required_ensemble = info["ensemble"]
    
    if ensemble != required_ensemble:
        raise ConfigError(
            f"md.ensemble='{ensemble}' does not match md.method='{method}' "
            f"(method requires ensemble '{required_ensemble}')."
        )

    total_steps = _require_int_gt(cfg, "md.total_steps", 0)
    timestep_fs = _require_num_gt(cfg, "md.timestep_fs", 0.0)

    # state
    if ensemble in ("nvt", "npt"):
        _require_num_gt(cfg, "state.temperature_K", 0.0)

    if ensemble == "npt":
        _require_num(cfg, "state.pressure_bar")
    
    if method == "velocity_verlet":
        # NVE: no extra parameters beyond timestep.
        pass

    elif method == "langevin":
        _require_num_gt(cfg, "thermostat.langevin.friction_per_fs", 0.0)

    elif method == "nose_hoover_chain_nvt":
        _require_num_gt(cfg, "thermostat.nose_hoover_chain.tdamp_fs", 0.0)
        _require_int_gt(cfg, "thermostat.nose_hoover_chain.tchain", 0)
        _require_int_gt(cfg, "thermostat.nose_hoover_chain.tloop", 0)

    elif method == "bussi":
        _require_num_gt(cfg, "thermostat.bussi.taut_fs", 0.0)

    elif method == "andersen":
        _require_num_gt(cfg, "thermostat.andersen.andersen_prob", 0.0)
        if _require_num(cfg, "thermostat.andersen.andersen_prob") > 1.0:
            raise ConfigError("thermostat.andersen.andersen_prob must be <= 1.0")

    elif method == "nvt_berendsen":
        _require_num_gt(cfg, "thermostat.berendsen.taut_fs", 0.0)

    # -------- NPT methods --------
    elif method == "npt_berendsen":
        _require_num_gt(cfg, "barostat.berendsen.taup_fs", 0.0)
        _require_num_gt(cfg, "barostat.berendsen.taut_fs", 0.0)  # <-- see note below
        _require_num_gt(cfg, "barostat.berendsen.compressibility_per_bar", 0.0)

    elif method in ("isotropic_mtk", "mtk"):
        _require_num_gt(cfg, "thermostat.nose_hoover_chain.tdamp_fs", 0.0)
        _require_int_gt(cfg, "thermostat.nose_hoover_chain.tchain", 0)
        _require_int_gt(cfg, "thermostat.nose_hoover_chain.tloop", 0)

        _require_num_gt(cfg, "barostat.mtk.pdamp_fs", 0.0)
        _require_int_gt(cfg, "barostat.mtk.pchain", 0)
        _require_int_gt(cfg, "barostat.mtk.ploop", 0)

    elif method == "langevin_baoab":
        # These are optional in ASE, but validate if user provides them.
        # (If you later add defaults, switch to _require_num_gt)
        if "barostat" in cfg and "baoab" in cfg["barostat"]:
            baoab = cfg["barostat"]["baoab"]
            if "T_tau_fs" in baoab:
                _require_num_gt(cfg, "barostat.baoab.T_tau_fs", 0.0)
            if "P_tau_fs" in baoab:
                _require_num_gt(cfg, "barostat.baoab.P_tau_fs", 0.0)
            if "P_mass_factor" in baoab:
                _require_num_gt(cfg, "barostat.baoab.P_mass_factor", 0.0)

    elif method == "melchionna":
        # Optional knobs; validate if present
        if "barostat" in cfg and "melchionna" in cfg["barostat"]:
            mel = cfg["barostat"]["melchionna"]
            if "ttime_fs" in mel:
                _require_num_gt(cfg, "barostat.melchionna.ttime_fs", 0.0)
            if "pfactor" in mel:
                _require_num_gt(cfg, "barostat.melchionna.pfactor", 0.0)


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
