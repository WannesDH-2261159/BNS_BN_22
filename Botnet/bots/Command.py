from enum import Enum

class Command(Enum):
    STATUS = "status"
    PAYLOAD = "payload"
    EXECUTE = "execute"
    STOP = "stop"
    REMOVE = "remove"
    NONE = "none"
