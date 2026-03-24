import subprocess

# Handles the tracking of currently executing programs on the bot's system, allowing for management and monitoring of active processes
class ExecutingProgramHandler:
    def __init__(self):
        self.__mapNameToProgram = {}
        self.__execPrograms = []

    def add_program(self, id):
        self.__execPrograms.append(id)

    def remove_program(self, id):
        if id in self.__execPrograms:
            self.__execPrograms.remove(id)

    def is_program_running(self, id):
        return id in self.__execPrograms
        
    def stop_all_programs(self):
        print("Stopping programs...")
        for prgrm in self.__execPrograms:
            try:
                prgrm.send_signal(1)  # Send CTRL_BREAK_EVENT to gracefully stop the process
                prgrm.wait(timeout=5)
            except subprocess.TimeoutExpired:
                prgrm.kill()
                prgrm.wait()
            except Exception as e:
                print(f"Error stopping program: {e}")

        print("All programs  stopped successfully.")
        self.__execPrograms.clear()