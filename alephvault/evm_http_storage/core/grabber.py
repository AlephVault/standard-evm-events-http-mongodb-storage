import web3
import json


def grab_all_events_since(gateway_url: str, events_settings: dict, state: dict):
    """
    Grabs all the events since a certain limit, per state.
    :param gateway_url: The URL of the gateway to use (it must support event logs retrieval).
    :param events_settings: The dictionary with the settings to use.
    :param state: The state (a mapping of eventKey => startBlock) to use.
    :return: A dictionary of blockNumber => events.
    """

    client = web3.Web3(web3.providers.HTTPProvider(gateway_url))
    events_list = {}
    for event_key, event_settings in events_settings.items():
        contract = client.eth.contract(web3.Web3.toChecksumAddress(event_settings['address']),
                                       abi=json.dumps(event_settings['abi']))
        event_filter = getattr(contract.events, event_settings['event']).createFilter(
            fromBlock=state.get(event_key, '0x0')
        )
        for event in event_filter.get_all_entries():
            entry = {**{
               k: v for k, v in event.items() if k in {"blockNumber", "transactionIndex", "logIndex", "args"}
            }, "eventKey": event_key}
            events_list.setdefault(entry["blockNumber"], []).append(entry)
    return events_list
