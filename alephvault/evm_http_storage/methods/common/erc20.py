import os
import logging
from flask import jsonify
from alephvault.evm_http_storage.schemas.contracts import WORKER_SCHEMA
from alephvault.http_storage.types.method_handlers import MethodHandler
from pymongo import MongoClient


class ERC20ResetCache(MethodHandler):
    """
    Resets all the cache settings for a given ERC20-typed event-key.
    It needs many things to work appropriately:
    - On request: The contract-key whose cache is being cleared.
    - On constructor: The db/collection holding the state.
    - Also needed on request: All the event-keys that are related
      to the contract-key

    # TODO this is wrong. A refactor is needed.
    """

