"""
These schemas define the configuration of event settings.
Each event contains an ABI (which is converted to a list
  by using `json.loads(abi)` over the original string
  value and using that result in the spec itself - it
  will be converted to string later when needed to be
  used as argument), a contract address (a valid, but
  not checksum-verified, hexadecimal address), and the
  handler that will be used to process each event in the
  list of events of a given block.
"""


EVENT = {
    "address": {
        "type": "string",
        "required": True,
        "regex": "0x[a-fA-F0-9]{40}"
    },
    "abi": {
        "type": "list",
        "required": True,
        "schema": {
            "type": "dict",
            "allow_unknown": True,
            "schema": {
                "name": {
                    "type": "string",
                    "required": True,
                    "regex": "[a-z][A-Z0-9_]+"
                },
                "type": {
                    "type": "string",
                    "allowed": ["constructor", "function", "fallback", "receive", "event"]
                },
            }
        }
    },
    "handler": {
        "type": "event-handler",
        "required": True
    }
}

EVENT_SETTINGS = {
    "type": "dict",
    "keysrules": {
        "type": "string",
        "regex": "[a-zA-Z][a-zA-Z0-9_-]+"
    },
    "valuesrules": {
        "type": "dict",
        "schema": EVENT
    }
}