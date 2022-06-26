from alephvault.evm_http_storage.validation import WorkerSettingsValidator
from alephvault.http_storage.types.method_handlers import MethodHandler
from pymongo import MongoClient


class EventGrabberWorker(MethodHandler):
    """
    An event grabber is a method handler that, taking the events
    settings, retrieves the blockchain events after the current
    state, processes them, and updates the state in the blockchain.
    """

    def __init__(self, events_settings: dict):
        """
        Creates an event grabber handler by using certain events settings.
        :param events_settings: The events settings to use.
        """

        # self._events_settings = events_settings
        # validator = WorkerSettingsValidator()
        # output = validator.validate(events_settings)

    def __call__(self, client: MongoClient, resource: str, method: str, db: str, collection: str, filter: dict):
        """

        :param client:
        :param resource:
        :param method:
        :param db:
        :param collection:
        :param filter:
        :return:
        """