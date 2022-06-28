from alephvault.evm_http_storage.methods.common.erc721 import ERC20Collections, ERC20CollectionOf


def make_evm_erc721_balance_resource(db_name: str = 'evm', erc721balance_collection_name: str = 'erc721-ownership',
                                     erc721balance_resource_name: str = "evm-erc721-ownership"):
    """
    Makes an EVM resource to track token ownerships of an ERC-721 smart contract.
    :return: A dictionary with the resource configuration.
    """

    return {
        erc721balance_resource_name: {
            "db": db_name,
            "collection": erc721balance_collection_name,
            "type": "list",
            "verbs": ["list", "read"],
            "schema": {
                "contract-key": {
                    "type": "string",
                    "required": True,
                    "regex": "[a-zA-Z][a-zA-Z0-9-]+"
                },
                "owner": {
                    "type": "string",
                    "required": True,
                    "regex": "0x[a-fA-F0-9]{40}"
                },
                "token": {
                    "type": "string",
                    "required": True,
                    "regex": "0x[a-f0-9]{1,64}"
                }
            },
            "indexes": {
                "lookup": {
                    "unique": True,
                    "fields": ["contract-key", "token"]
                },
                "owned-list": {
                    "fields": ["contract-key", "owner"]
                }
            },
            "methods": {
                "collections": {
                    "type": "view",
                    "handler": ERC20Collections()
                },
                "collection-of": {
                    "type": "view",
                    "handler": ERC20CollectionOf()
                }
            }
        }
    }
