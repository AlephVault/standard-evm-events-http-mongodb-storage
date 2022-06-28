from .abi import ERC20ABI, ERC721ABI, ERC1155ABI
from .erc1155balance_handler import ERC1155BalanceHandler
from .erc20balance_handler import ERC20BalanceHandler
from .erc721balance_handler import ERC721BalanceHandler


def erc20_transfer_event(address: str, contract_key: str):
    """
    Creates an event entry for an ERC-20's Transfer event.
    :param address: The contract address.
    :param contract_key: The key to associate to this contract.
    :return: The event entry.
    """

    return {
        'address': address,
        'event': 'Transfer',
        'abi': ERC20ABI,
        'handler': ERC20BalanceHandler(contract_key)
    }


def erc721_transfer_event(address: str, contract_key: str):
    """
    Creates an event entry for an ERC-721's Transfer event.
    :param address: The contract address.
    :param contract_key: The key to associate to this contract.
    :return: The event entry.
    """

    return {
        'address': address,
        'event': 'Transfer',
        'abi': ERC721ABI,
        'handler': ERC721BalanceHandler(contract_key)
    }


def erc1155_transfer_single_event(address: str, contract_key: str):
    """
    Creates an event entry for an ERC-1155's TransferSingle event.
    :param address: The contract address.
    :param contract_key: The key to associate to this contract.
    :return: The event entry.
    """

    return {
        'address': address,
        'event': 'TransferSingle',
        'abi': ERC1155ABI,
        'handler': ERC1155BalanceHandler(contract_key)
    }


def erc1155_transfer_batch_event(address: str, contract_key: str):
    """
    Creates an event entry for an ERC-1155's TransferBatch event.
    :param address: The contract address.
    :param contract_key: The key to associate to this contract.
    :return: The event entry.
    """

    return {
        'address': address,
        'event': 'TransferBatch',
        'abi': ERC1155ABI,
        'handler': ERC1155BalanceHandler(contract_key)
    }
