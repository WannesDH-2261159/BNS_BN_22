from bots.Bot import Bot
import ctypes

from pyshortcuts import make_shortcut
import os
import sys

def check_shortcut_exists():
    shortcut_path = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows',
                                 'Start Menu', 'Programs', 'Startup', 'BotnetStartup.lnk')
    return os.path.exists(shortcut_path)

def create_shortcut():
    destination = os.path.join(os.path.join(os.environ['USERPROFILE']), 'AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup')
    make_shortcut(sys.argv[0], name="BotnetStartup", folder=destination)

def ask_for_startup_shortcut():
    ans = notification(0, "Botnet want to run at startup.\n\nadd to startup apps?", "Botnet notification", 4)
    if ans == 6:
        print("OK")
        create_shortcut()

def ask_to_become_bot():
    ans = notification(0, "Running this software will make you part of a botnet.\n\nRun botnet software?", "Botnet notification", 4)
    if ans == 6:
        return True
    elif ans == 7:
        return False

def handle_startup_bot():
    if not check_shortcut_exists():
        ask_for_startup_shortcut()
    
    test = Bot()


# BOT STARTUP EXECUTION CODE
if __name__ == "__main__":
    notification = ctypes.windll.user32.MessageBoxW
    notification.restype = ctypes.c_int

    becomeBot = ask_to_become_bot()
    if becomeBot:
        handle_startup_bot()
    else:
        sys.exit(0)