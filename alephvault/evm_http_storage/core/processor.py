from pymongo import MongoClient
from pymongo.collection import Collection


def _tohex(value: int):
    """
    Normalizes an integer value to its hexadecimal representation.
    :param value: The value to normalize to hex.
    :return: The normalized hexadecimal value.
    """

    h = hex(value)[2:]
    return "0x" + ("0" * max(0, 64 - len(h))) + h


def process_full_events_list(events_list: dict, events_settings: dict, client: MongoClient,
                             state_collection: Collection, state: dict):
    """
    Processes all the events in the incoming list. This is done according
    to a given current state (and state collection), its state collection
    (to update it appropriately), and a given client to be used into the
    specific event handlers.
    :param events_list: The list of events to process. This is actually a dictionary.
    :param events_settings: A dictionary with the per-event settings.
    :param client: A MongoDB client.
    :param state_collection: A collection, related to the client, into which
      the state will be saved.
    :param state: The current state, which is periodically updated and pushed.
    :return: The events that were effectively synchronized, and whether an exception
      occurred in the processing.
    """

    all_processed_events = []

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
                    processed_events = []
                    for event in events:
                        handler = events_settings[event['eventKey']]["handler"]
                        processed_events.append(handler(client, session, event))
                    # Update and store the states.
                    state[event['eventKey']] = _tohex(blockNumber + 1)
                    state_collection.replace_one({}, {"value": state}, session=session)
                    # Update response.
                    all_processed_events.extend(processed_events)
        return all_processed_events, None
    except Exception as e:
        return all_processed_events, e
