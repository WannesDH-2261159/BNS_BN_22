import ctypes
notification = ctypes.windll.user32.MessageBoxW
notification.restype = ctypes.c_int

ans = notification(0, "You are part of a botnet.\nRun botnet software?", "Botnet notification", 4)
if ans == 6:
    print("OK")
elif ans == 7:
    print("No")