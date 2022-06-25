from pymongo import MongoClient


def _tohex(value: int):
    """
    Normalizes an integer value to its hexadecimal representation.
    :param value: The value to normalize to hex.
    :return: The normalized hexadecimal value.
    """

    h = hex(value)[2:]
    return "0x" + ("0" * max(0, 64 - len(h))) + h


def process_full_events_list(events_list: dict, events_settings: dict, client: MongoClient,
                             cache_db: str, cache_state_collection: str, state: dict):
    """
    Processes all the events in the incoming list. This is done according
    to a given current state (and state collection), its state collection
    (to update it appropriately), and a given client to be used into the
    specific event handlers.
    :param events_list: The list of events to process. This is actually a dictionary.
    :param events_settings: A dictionary with the per-event settings.
    :param client: A MongoDB client.
    :param cache_db: The database name, related to the given client, that stores all
      these cache settings.
    :param cache_state_collection: The collection, related to the given client and db,
      that stores the state. Only one single entry should exist there.
    :param state: The current state, which is periodically updated and pushed.
    :return: The events that were effectively synchronized, and whether an exception
      occurred in the processing.
    """

    state_collection = client[cache_db][cache_state_collection]
    processed_events = []

    try:
        with client.start_session() as session:
            # Inside this session, all the events will be iterated.
            # The first iteration level, which will correspond to
            # a MongoDB Transaction, belongs to the block number.
            for blockNumber in sorted(events_list.keys()):
                with session.start_transaction():
                    # Processes all the events. The events themselves
                    # will NOT be stored directly, but the handlers
                    # MAY cause some data be stored.
                    #
                    # Each event is expected to have the following
                    # fields:
                    # - "args" (a dictionary - it contains data that
                    #   might require normalization). To be processed
                    #   by the handlers.
                    # - "blockNumber": An arbitrary-length integer
                    #   number with the block number. If stored, it
                    #   should be normalized (to hex string).
                    # - "transactionIndex": An arbitrary-length integer
                    #   number, but typically -in practice- in the range
                    #   of 32 bits. If stored, in the future it might
                    #   need of normalization (to hex string).
                    # - "logIndex": An arbitrary-length integer number,
                    #   but typically -in practice- in the range of 32
                    #   bits. If stored, in the future it might need of
                    #   normalization (to hex string).
                    # - "eventKey": A unique event key, among the other
                    #   registered events (which are a combination of
                    #   the event address, the ABI, and the name of the
                    #   event we're interested in retrieving).
                    events = sorted(events_list[blockNumber], key=lambda evt: (evt['transactionIndex', 'logIndex']))
                    for event in events:
                        handler = events_settings[event['eventKey']]
                        handler(client, session, event)
                    # Update and store the states.
                    state[event['eventKey']] = _tohex(blockNumber)
                    state_collection.replace_one({}, {"value": state}, session=session)
                    # Update response.
                    processed_events.extend(events)
        return processed_events, None
    except Exception as e:
        return processed_events, e
