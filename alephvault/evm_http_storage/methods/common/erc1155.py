from flask import request
from cerberus import Validator
from alephvault.http_storage.core.responses import format_invalid, ok
from alephvault.http_storage.types.method_handlers import MethodHandler
from pymongo import MongoClient


class ERC1155BalanceOf(MethodHandler):
    """
    Gets the balance of a token for an account in an ERC-1155 contract.
    """

    SCHEMA = {
        "contract-key": {
            "type": "string",
            "required": True
        },
        "owner": {
            "type": "string",
            "required": True,
            "regex": r"0x[a-fA-F0-9]{40}"
        },
        "token": {
            "type": "string",
            "required": True,
            "regex": "0x[a-f0-9]{1,64}"
        }
    }

    def __call__(self, client: MongoClient, resource: str, method: str, db: str, collection: str, filter: dict):
        validator = Validator(self.SCHEMA)
        if not validator.validate({**request.args}):
            return format_invalid(validator.errors)
        entry = client[db][collection].find_one({**filter, "contract-key": validator.document["contract-key"],
                                                 "owner": validator.document["owner"],
                                                 "token": validator.document["token"]})
        return ok({"amount": (entry or {}).get("amount", 0)})


class ERC1155BalancesOf(MethodHandler):
    """
    Gets the balances of all the tokens for an account in an ERC-1155 contract.
    """

    SCHEMA = {
        "contract-key": {
            "type": "string",
            "required": True
        },
        "owner": {
            "type": "string",
            "required": True,
            "regex": r"0x[a-fA-F0-9]{40}"
        },
        "offset": {
            "type": "string",
            "required": True,
            "regex": r"\d+",
            "default": "0"
        },
        "limit": {
            "type": "string",
            "required": True,
            "regex": r"0*[1-9]\d*",
            "default": "20"
        }
    }

    def __call__(self, client: MongoClient, resource: str, method: str, db: str, collection: str, filter: dict):
        validator = Validator(self.SCHEMA)
        if not validator.validate({**request.args}):
            return format_invalid(validator.errors)
        query = client[db][collection].find({**filter, "contract-key": validator.document["contract-key"],
                                             "owner": validator.document["owner"]})
        query = query.skip(int(validator.document["offset"])).limit(int(validator.document["limit"]))
        return ok([{"token": e.get("token"), "amount": e.get("amount")} for e in query])


class ERC1155Balances(MethodHandler):
    """
    Gets the balances of all the tokens and accounts in an ERC-1155 contract, by paging.
    """

    SCHEMA = {
        "contract-key": {
            "type": "string",
            "required": True
        },
        "offset": {
            "type": "string",
            "required": True,
            "regex": r"\d+",
            "default": "0"
        },
        "limit": {
            "type": "string",
            "required": True,
            "regex": r"0*[1-9]\d*",
            "default": "20"
        }
    }

    def __call__(self, client: MongoClient, resource: str, method: str, db: str, collection: str, filter: dict):
        validator = Validator(self.SCHEMA)
        if not validator.validate({**request.args}):
            return format_invalid(validator.errors)
        query = client[db][collection].find({**filter, "contract-key": validator.document["contract-key"]})
        query = query.skip(int(validator.document["offset"])).limit(int(validator.document["limit"]))
        return ok([{"token": e.get("token"), "owner": e.get("owner"), "amount": e.get("amount")} for e in query])
