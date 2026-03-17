from bots.Bot import Bot
import ctypes

from pyshortcuts import make_shortcut
import os
import sys

if __name__ == "__main__":
    notification = ctypes.windll.user32.MessageBoxW
    notification.restype = ctypes.c_int

    ans = notification(0, "You are part of a botnet.\nRun botnet software?", "Botnet notification", 4)
    if ans == 6:
        print("OK")
        # Ask to create startup shortcut
        ans = notification(0, "You are part of a botnet.\nAdd to startup apps?", "Botnet notification", 4)
        if ans == 6:
            print("OK")
            destination = os.path.join(os.path.join(os.environ['USERPROFILE']), 'AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup')
            make_shortcut(sys.argv[0], name="BotnetStartup", folder=destination)
        
        # Start bot
        test = Bot()
    
    elif ans == 7:
        print("No")
    
