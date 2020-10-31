"""Module used to suggest datapoints for a platform."""
from importlib import import_module


def _suggest_defaults(suggestions, dps_strings):
    """Return datapoint suggestions for options."""

    def _match(suggestion):
        for dps_str in dps_strings:
            if dps_str.startswith(f"{suggestion} "):
                return dps_str
        return None

    output = {}
    for conf, conf_suggestion in suggestions.items():
        for suggestion in conf_suggestion:
            match = _match(suggestion)
            if match:
                output[conf] = match
                break
    return output


def suggest(platform, dps_strings):
    """Suggest datapoints for a platform."""
    integration_module = ".".join(__name__.split(".")[:-1])
    module = import_module("." + platform, integration_module)

    if hasattr(module, "DP_SUGGESTIONS"):
        return _suggest_defaults(module.DP_SUGGESTIONS, dps_strings)
    return {}
