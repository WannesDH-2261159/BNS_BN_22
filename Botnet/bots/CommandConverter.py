from bots.Command import Command

class CommandConverter:
    def convert_cmd_to_enum(self, cmd: str):
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