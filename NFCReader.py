import os
import threading
from typing import List

from smartcard import util
from smartcard.CardRequest import CardRequest
from smartcard.CardType import AnyCardType
from smartcard.Exceptions import CardRequestTimeoutException
from smartcard.scard import *

from PythonNFCReader.CardListener import CardListener


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
            os._exit(os.EX_SOFTWARE)

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


class CardConnectionManager:
    def __init__(self):
        self.listeners: List[CardListener] = []
        self.nfc_thread = None
        self.listener_thread = None
        self.nfc_reader = None
        pass

    def register_listener(self, card_listener: CardListener) -> None:
        if card_listener is not None:
            self.listeners.append(card_listener)

    def start_nfc_reader(self):
        # Create thread that will block while waiting for a card
        self.nfc_thread = threading.Thread(name="NFC_reader",
                                           target=self.__generate_nfc_reader, daemon=True)
        self.nfc_thread.start()

        # Create thread that will listen for the nfc_thread to finish
        self.listener_thread = threading.Thread(name="NFC_reader_monitor",
                                                target=self.__monitor_nfc_reader,
                                                args=(self.nfc_thread,), daemon=True)
        self.listener_thread.start()

    def __generate_nfc_reader(self):
        # Blocking call (as it will start waiting for a card)
        self.nfc_reader = NFCReader()

    def __monitor_nfc_reader(self, thread: threading.Thread) -> None:
        # Wait for the thread to finish
        thread.join()

        uid = self.nfc_reader.get_uid()

        # Check if we got a valid uid (of the card)
        if uid is not None and uid != "":
            # Notify listeners that we received a new card
            self.__notify_listeners(self.nfc_reader.get_uid().replace(" ", ""))

        # Start waiting for a new card after 1 second.
        threading.Timer(1.0, self.start_nfc_reader).start()

    def __notify_listeners(self, uid: str):
        for listener in self.listeners:
            listener.card_is_presented(uid)
