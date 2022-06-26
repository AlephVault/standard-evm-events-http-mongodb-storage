from alephvault.evm_http_storage.methods import EventGrabberWorker


def make_evm_resource(events_settings: dict, db_name: str = 'evm',
                      state_collection_name: str = 'state',
                      state_resource_name: str = "evm-state"):
    """
    Makes a dictionary holding a single resource. This dictionary
    will be validated using the Remote Storage's mongodb validator.
    :param events_settings: The settings that define the events
      that will be fetched on a work loop.
    :param db_name: The name of the DB to use for the state
      resource. It must satisfy the Remote Storage's rules
      for the MongoDB identifiers.
    :param state_collection_name: The name of the collection
      to use for the state resource. It must satisfy the Remote
      Storage's rules for the MongoDB identifiers.
    :param state_resource_name: The name for the state resource.
    :return: A dictionary with the resource configuration.
    """

    return {
        state_resource_name: {
            "db": db_name,
            "collection": state_collection_name,
            "type": "simple",
            "verbs": ["read"],
            "methods": {
                "grab": {
                    "type": "operation",
                    "handler": EventGrabberWorker(events_settings)
                }
            },
            "schema": {
                "value": {
                    "type": "dict",
                    "keysrules": {
                        "type": "string",
                        "regex": "[a-zA-Z][a-zA-Z0-9_-]+"
                    },
                    "valuesrules": {
                        "type": "string",
                        "regex": "0x[0-9a-f]{1,64}"
                    }
                }
            }
        }
    }
