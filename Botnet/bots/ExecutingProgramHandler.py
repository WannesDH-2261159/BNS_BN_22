import subprocess

# Handles the tracking of currently executing programs on the bot's system, allowing for management and monitoring of active processes
class ExecutingProgramHandler:
    def __init__(self):
        self.executing_programs = []

    def add_program(self, id):
        self.executing_programs.append(id)

    def remove_program(self, id):
        if id in self.executing_programs:
            self.executing_programs.remove(id)

    def is_program_running(self, id):
        return id in self.executing_programs
        
    def stop_all_programs(self):
        print("Stopping programs...")
        for prgrm in self.executing_programs:
            try:
                prgrm.send_signal(1)  # Send CTRL_BREAK_EVENT to gracefully stop the process
                prgrm.wait(timeout=5)
            except subprocess.TimeoutExpired:
                prgrm.kill()
                prgrm.wait()
            except Exception as e:
                print(f"Error stopping program: {e}")

        print("All programs  stopped successfully.")
        self.executing_programs.clear()