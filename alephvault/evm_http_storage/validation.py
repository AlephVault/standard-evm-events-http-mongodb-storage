from cerberus import Validator, TypeDefinition
from alephvault.evm_http_storage.core.event_handler import EventHandler
from alephvault.evm_http_storage.schemas.events import WORKER_SCHEMA


class WorkerSettingsValidator(Validator):
    """
    This validator is NOT used in the context of the web application,
    but instead in the context of the settings that will be used for
    the whole loop processing (the schema for the web app is standard
    to the HTTP MongoDB Remote Storage and will be defined and then
    validated elsewhere).
    """

    types_mapping = {
        **Validator.types_mapping,
        "event-handler": TypeDefinition("event-handler", (EventHandler,), ())
    }

    def __init__(self):
        super().__init__(WORKER_SCHEMA)
