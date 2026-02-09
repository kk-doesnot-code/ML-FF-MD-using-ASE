from __future__ import annotations


def _deep_merge(base: dict, override: dict) -> dict:
    """
    Recursively merge two dictionaries.

    Rules:
    - If a key is missing in override, keep base value
    - If a key exists in override:
        - if both values are dict -> merge recursively
        - else -> override wins
    """
    result = {}

    for key, base_value in base.items():
        result[key] = base_value

    for key, override_value in override.items():
        if key in result:
            current_value = result[key]

            if isinstance(current_value, dict) and isinstance(override_value, dict):
                merged_value = _deep_merge(current_value, override_value)
                result[key] = merged_value
            else:
                result[key] = override_value
        else:
            result[key] = override_value

    return result


def get_defaults_for_method(method: str) -> dict:
    """
    Return default parameter blocks for a given md.method.
    """
    if method == "isotropic_mtk":
        return {
            "thermostat": {
                "nose_hoover_chain": {
                    "tdamp_fs": 100.0,
                    "tchain": 3,
                    "tloop": 1,
                }
            },
            "barostat": {
                "mtk": {
                    "pdamp_fs": 1000.0,
                    "pchain": 3,
                    "ploop": 1,
                }
            },
        }
    
    if method == "npt_berendsen":
        return {
            "barostat": {
                "berendsen": {
                    "taut_fs": 500.0,
                    "taup_fs": 1000.0,
                    "compressibility_per_bar": 4.57e-5,
                }
            }
        }

    if method == "langevin":
        return {
            "thermostat": {
                "langevin": {
                    "friction_per_fs": 0.01
                }
            }
        }

    if method == "nose_hoover_chain_nvt":
        return {
            "thermostat": {
                "nose_hoover_chain": {
                    "tdamp_fs": 100.0,
                    "tchain": 3,
                    "tloop": 1,
                }
            }
        }

    if method == "bussi":
        return {
            "thermostat": {
                "bussi": {
                    "taut_fs": 100.0
                }
            }
        }

    if method == "andersen":
        return {
            "thermostat": {
                "andersen": {
                    "andersen_prob": 0.002
                }
            }
        }

    if method == "nvt_berendsen":
        return {
            "thermostat": {
                "berendsen": {
                    "taut_fs": 100.0
                }
            }
        }


    # No defaults for unknown methods yet
    return {}


def apply_defaults(cfg: dict) -> dict:
    """
    Apply method-specific defaults to the user config.
    User values always override defaults.
    """
    md_cfg = cfg.get("md", {})
    method = md_cfg.get("method", None)

    if method is None:
        return cfg

    defaults = get_defaults_for_method(method)
    merged = _deep_merge(defaults, cfg)

    return merged
