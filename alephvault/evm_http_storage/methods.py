import os
import logging
from flask import jsonify
from alephvault.evm_http_storage.core import loop
from alephvault.evm_http_storage.schemas.events import WORKER_SCHEMA
from alephvault.evm_http_storage.validation import WorkerSettingsValidator
from alephvault.http_storage.types.method_handlers import MethodHandler
from pymongo import MongoClient


LOGGER = logging.getLogger(__name__)


class EventGrabberWorker(MethodHandler):
    """
    An event grabber is a method handler that, taking the events
    settings, retrieves the blockchain events after the current
    state, processes them, and updates the state in the blockchain.
    """

    def __init__(self, grabber_settings: dict):
        """
        Creates an event grabber handler by using certain events settings.
        :param grabber_settings: The events settings to use.
        """

        validator = WorkerSettingsValidator(WORKER_SCHEMA)
        valid = validator.validate(grabber_settings)
        if not valid:
            raise ValueError(validator.errors)
        self._events_settings = validator.document['events']
        self._gateway_url = os.environ[validator.document['gateway_url_environment_var']]

    def __call__(self, client: MongoClient, resource: str, method: str, db: str, collection: str, filter: dict):
        """
        Processes a request to get the last events and process them.
        :param client: The MongoDB client to use.
        :param resource: The name of the related resource. Not used here.
        :param method: The name of the related method. Not used here.
        :param db: The name of the related resource's database.
        :param collection: The name of the related resource's collection.
        :param filter: The filter of the related resource. Not used here.
        :return: A pair of processed element and an HTTP code: 200 if no error, 500 if error.
        """

        processed, error = loop(gateway_url=self._gateway_url, events_settings=self._events_settings,
                                client=client, cache_db=db, cache_state_collection=collection)
        if error:
            LOGGER.error(f"An error occurred while running the loop: {type(error).__name__} -> {error}")
            return jsonify(processed), 200
        else:
            return jsonify(processed), 500
