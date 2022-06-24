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