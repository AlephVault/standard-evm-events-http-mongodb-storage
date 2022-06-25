from .events import EVENTS_SETTINGS


# This schema is meant for the worker loop
WORKER_SCHEMA = {
    "events": EVENTS_SETTINGS,
    "gateway_url_environment_var": {
        "type": "string",
        "required": True,
        "regex": r"[a-zA-Z_][a-zA-Z0-9_]"  # The url itself will satisfy: r"https?://[\w_-]+(\.[\w_-]+)*(:\d+)/?"
    }
}
