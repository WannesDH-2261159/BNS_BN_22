import subprocess

# Handles the tracking of currently executing programs on the bot's system, allowing for management and monitoring of active processes
class ExecutingProgramHandler:
    """ --- PRIVATE METHODS --- """
    def __init__(self):
        self.__execPrograms = {}

    def __kill_program(self, prgrm):
        try:
            prgrm.send_signal(1)  # Send CTRL_BREAK_EVENT to gracefully stop the process
            prgrm.wait(timeout=5)
        except subprocess.TimeoutExpired:
            prgrm.kill()
            prgrm.wait()
        except Exception as e:
            print(f"Error stopping program: {e}")


    """ --- PUBLIC METHODS --- """
    # Return a list of program names
    def get_running_programs(self):
        return self.__execPrograms.keys()


    def stop_all_programs(self):
        for prgrm in self.__execPrograms.values():
            try:
                self.__kill_program(prgrm)
            except Exception as e:
                print (f"Error stopping prgrm {e}")
        self.__execPrograms.clear()


    def stop_program(self, name: str):
        prgrm = self.__execPrograms.get(name)
        try:
            self.__kill_program(prgrm)
        except Exception as e:
            print (f"Error stopping prgrm {e}")
        self.__execPrograms.pop(name)


    def add_program(self, id, name: str):
        self.__execPrograms.update({name: id})