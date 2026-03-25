import platform

class MachineInfo:
    def __init__(self):
        self.__init_machine_info()

    def __init_machine_info(self):
        # DEVICE ID
        self.MAC_ADDR = "00:1A:2B:3C:4D:5X"  # Placeholder for MAC address retrieval logic
        self.IP_ADDR = "192.168.1.101"  # Placeholder for IP address retrieval logic

        # DEVICE INFO
        self.ARCHITECTURE = platform.machine()
        self.CPU_INFO = platform.processor()

        # OS INFO
        self.OS_NAME = platform.system()
        self.OS_VERSION = platform.release()

    def get_machine_info(self):
        return {
            "MAC_ADDR": self.MAC_ADDR,
            "IP_ADDR": self.IP_ADDR,
            "ARCHITECTURE": self.ARCHITECTURE,
            "CPU_INFO": self.CPU_INFO,
            "OS_NAME": self.OS_NAME,
            "OS_VERSION": self.OS_VERSION
        }