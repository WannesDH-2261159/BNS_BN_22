from bots import Cryptographic
from bots.Command import Command

# Dictionary for Notification Events
from bots.dictionaries.NotficationEvents import Events

class NotificationBuilder:
    def __init__(self, crypt: Cryptographic):
        self.crypt = crypt

    def build_status_notification(self, data: tuple, event: str = "Rebooting..."):
        MAC = data["MAC_ADDR"]
        IP = data["IP_ADDR"]
        OS_NAME = data["OS_NAME"]
        OS_VERSION = data["OS_VERSION"]
        ARCHITECTURE = data["ARCHITECTURE"]
        CPU_INFO = data["CPU_INFO"]

        # Encrypt the Device ID before including it in the notification
        DeviceID = f"{MAC}-{IP}"
        DeviceID = self.crypt.encrypt(DeviceID)

        lines = [
            f"{event}",
            "",
            f"  Device ID : {DeviceID}",
            f"  OS        : {OS_NAME} {OS_VERSION}",
            f"  Arch      : {ARCHITECTURE}",
            f"  CPU       : {CPU_INFO}",
        ]
        return "\n".join(lines)

    def build_notification(self, data: str, type: Command):
        if type == Command.STATUS:
            return self.build_status_notification(data, Events["START"])
        else:
            return "UNKNOWN COMMAND"