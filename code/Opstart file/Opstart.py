from pyshortcuts import make_shortcut
import sys
import os

make_shortcut(sys.argv[0], name="BotnetStartup", folder='C:/Users/User/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup')

os.remove('C:/Users/User/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup/BotnetStartup.lnk')