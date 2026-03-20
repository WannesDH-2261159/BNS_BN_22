import Command

class NotificationBuilder:
    def __init__(self):
        pass

    def build_status_notification(self, data: tuple, event: str = "Rebooting..."):
        mac_ip, self.OS_NAME, self.OS_VERSION, self.ARCHITECTURE, self.CPU_INFO = data

        lines = [
            f"{event}",
            "",
            f"  Device ID : {mac_ip}",
            f"  OS        : {self.OS_NAME} {self.OS_VERSION}",
            f"  Arch      : {self.ARCHITECTURE}",
            f"  CPU       : {self.CPU_INFO}",
        ]
        return "\n".join(lines)

    def build_notification(self, data: str, type: Command):
        if type == Command.STATUS:
            return self.build_status_notification(data)
        else:
            return "UNKNOWN COMMAND"