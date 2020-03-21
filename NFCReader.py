from smartcard.scard import *
from smartcard.CardRequest import CardRequest
from smartcard.Exceptions import CardRequestTimeoutException
from smartcard.CardType import AnyCardType
from smartcard import util


# NFCReader class
# Is a blocking class until a card is presented to the card reader
#
class NFCReader:

    # Command to get UID (Serial number) of the presented NFC chip
    __GETUIDCOMMAND = "FF CA 00 00 00"

    # Card response values (in HEX)
    __uid = None
    __status = None

    # Reference to the connection of the card
    __service = None
    __request = None

    #
    # Resets variables before listening to establish a new connection
    #
    def __reset_local_vars(self):
        # If they are None, no work is required, else set them to None
        if self.__uid is not None and self.__status is not None and self.__service is not None:
            self.__service = None
            self.__uid = None
            self.__status = None
            self.__request = None

    #
    # Enables listening to NFC chip on card reader
    # var card_type: type of cards listening for
    #
    def enable_card_listener(self, card_type=AnyCardType()):
        # Check if resetting vars is required and if so, do so
        self.__reset_local_vars()

        # Setup a cardRequest: waiting infinitely for any card type
        self.__request = CardRequest(timeout=INFINITE, cardType=card_type)

        try:
            # Once a card is presented, initialize variables to setup connection
            self.__service = self.__request.waitforcard()
            self.__on_card_presented()
        except CardRequestTimeoutException:
            print("This should not happen: Timelimit reached for card presenting")
            exit(1)

    #
    # Callback function for when a card is presented
    # will establish a connection and attempt to send a command
    #
    # var service: the reference to the card
    #
    def __on_card_presented(self):
        # Setup connection and connect to the provided card
        connection = self.__service.connection
        connection.connect()
        # Send command to acquired connection
        self.__send_command(connection, self.__GETUIDCOMMAND)

    #
    # Send @command over @connection
    # Used to execute commands and store response values in class variables
    #
    # var connection: the connection over which to send the command
    # var command: the command to send over the aforementioned connection
    #
    def __send_command(self, connection, command):
        # Send GET_UID_COMMAND to the card reader
        get_uid_cmd = util.toBytes(command)
        # Retrieve response from APNU request
        data, sw1, sw2 = connection.transmit(get_uid_cmd)
        # Convert byte response data to HEX values
        self.__uid = util.toHexString(data)
        # Convert byte response values identifying success/failure to HEX values
        self.__status = util.toHexString([sw1, sw2])

    # Called upon creation of the class
    def __init__(self):
        # Specify card acceptance: any card accepted by the card reader
        self.enable_card_listener()

        # Print results
        # self.debug_print()

    #
    # Used to print the class' member variables
    # DEBUGGING PURPOSE
    #
    def debug_print(self):
        print("UID of card: " + self.__uid)
        print("Status of request: " + self.__status)

    #
    # Get reference to the card
    # DEBUGGING PURPOSE
    #
    def debug_get_service(self):
        return self.__service

    #
    # Get UID of card
    #
    def get_uid(self):
        return self.__uid

    #
    # reset connection
    #
    def reset_connection(self):
        self.__service = None


# create nfc_reader object
nfc_reader = NFCReader()
prev_uid = None
# uid = nfc_reader.get_uid()
# print(uid)

# For testing, print uid and restart listener
while True:
    uid = nfc_reader.get_uid()
    if prev_uid != uid:
        print(uid)
    prev_uid = uid
    # nfc_reader.reset_connection()
    nfc_reader.enable_card_listener()
