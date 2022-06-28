from alephvault.evm_http_storage.methods.common.erc20 import ERC20Balances, ERC20BalanceOf


def make_evm_erc20_balance_resource(db_name: str = 'evm', erc20balance_collection_name: str = 'erc20-balance',
                                    erc20balance_resource_name: str = "evm-erc20-balance"):
    """
    Makes an EVM resource to track balances of an ERC-20 smart contract.
    :return: A dictionary with the resource configuration.
    """

    return {
        erc20balance_resource_name: {
            "db": db_name,
            "collection": erc20balance_collection_name,
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
                "amount": {
                    # This is NOT hex-coded - just stringified.
                    "type": "string",
                    "required": True,
                    "regex": r"\d+"
                }
            },
            "indexes": {
                "lookup": {
                    "unique": True,
                    "fields": ["contract-key", "owner"]
                },
            },
            "methods": {
                "balances": {
                    "type": "view",
                    "handler": ERC20Balances()
                },
                "balance-of": {
                    "type": "view",
                    "handler": ERC20BalanceOf()
                }
            }
        }
    }
