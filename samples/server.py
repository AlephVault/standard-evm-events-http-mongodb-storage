import logging
from alephvault.http_storage.flask_app import StorageApp
from alephvault.evm_http_storage.core.common.token.shortcuts import erc20_transfer_event, erc721_transfer_event, \
    erc1155_transfer_single_event, erc1155_transfer_batch_event
from alephvault.evm_http_storage.schemas.resources import make_standard_evm_resources

logging.basicConfig()

ERC1155 = "0x83fD6d68C21c5a646971F8a788f3992365321304"
ERC721 = "0x0d938498e6C47DCc1c5a59Abc8aEf0eab7D115f4"
ERC20 = "0xb6eFBbc5466693166E25F17998ec0A90263C5582"

RESOURCES = make_standard_evm_resources({
    'events': {
        'erc20-transfer': erc20_transfer_event(ERC20, 'erc20-sample'),
        'erc721-transfer': erc721_transfer_event(ERC721, 'erc721-sample'),
        'erc1155-transfer-single': erc1155_transfer_single_event(ERC1155, 'erc1155-sample'),
        'erc155-transfer-batch': erc1155_transfer_batch_event(ERC1155, 'erc1155-sample')
    }
})


class SampleStorageApp(StorageApp):
    SETTINGS = {
        "auth": {
            "db": "auth-db",
            "collection": "api-keys"
        },
        "connection": {
            "host": "localhost",
            "port": 27017,
            "user": "admin",
            "password": "p455w0rd"
        },
        "resources": RESOURCES
    }

    def __init__(self, import_name: str = __name__):
        super().__init__(self.SETTINGS, import_name=import_name)
        try:
            self._client["auth-db"]["api-keys"].insert_one({"api-key": "abcdef"})
        except:
            pass


if __name__ == "__main__":
    app = SampleStorageApp()
    app.run("localhost", 6666)
