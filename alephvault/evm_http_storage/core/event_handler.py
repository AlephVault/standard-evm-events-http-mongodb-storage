from pymongo import MongoClient
from pymongo.client_session import ClientSession
from web3.datastructures import AttributeDict


class EventHandler:
    """
    A handler for a given event being received. It will take
    into account 3 things when an event is received: a client,
    a session (within that client), and an event to process.
    """

    def _is_zero(self, value):
        """
        Tests whether a value is a numeric 0 or 0.0, or perhaps
        a string representation of a 0 numeric value in any base.
        :param value: The value to test.
        :return: Whether it is zero or not.
        """

        if value == 0:
            return True

        for b in range(2, 37):
            try:
                if int(value, b) == 0:
                    return True
                else:
                    break
            except:
                pass

        return False

    def _get_arg(self, args, key):
        """
        Gets an argument from the args, by trying both `{key}` and `_{key}`
        as the key to test.
        :param args: The args to get an argument from
        :param key:
        :return:
        """

        if key in args:
            return args[key]
        else:
            return args.get("_" + key)

    def __call__(self, client: MongoClient, session: ClientSession, event: AttributeDict):
        """
        Processes an event inside a transaction. That transaction exists in a session,
        which is turn belongs to the client, and the given event will be processed by
        said transaction. This handler must process whatever it needs as given (e.g.
        for ERC-20 Transfer event, increment and decrement existing quantities, save
        for the fact of 0x0 addresses), and return whatever makes sense for the game
        to be notified about the changes.
        :param client: The MongoDB client to use.
        :param session: The current MongoDB session.
        :param event: The event being processed.
        :return: Whatever makes sense for the game.
        """

        raise NotImplementedError
