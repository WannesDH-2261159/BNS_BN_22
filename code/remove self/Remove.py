import os
import sys
import subprocess

def schedule_self_delete():
    exe_path = os.path.abspath(sys.argv[0])

    if os.name == "nt":  # Windows
        subprocess.Popen(
            f'cmd /c ping 127.0.0.1 -n 2 > nul & del "{exe_path}"',
            shell=True
        )
    else:  # Linux / macOS
        subprocess.Popen(
            f'sh -c "sleep 1 && rm \\"{exe_path}\\""',
            shell=True
        )

for i in range(100):
    print(i)

schedule_self_delete()

print("Program finished")