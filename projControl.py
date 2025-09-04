#!/usr/bin/python3
import json
import os
import sys

from pypjlink import Projector #pip install pypjlink2

VERSION = "2025.09.04"
print(f"projControl Version: {VERSION}")

def get_default_settings():
    """Returns a dictionary with the default settings."""
    return {
        "projectors" : [
            "192.168.60.30",
            "192.168.60.65",
            "192.168.60.142",
            "192.168.60.247"
        ] 
    }

def readConfig(settingsFile):
    
    if os.path.isfile(settingsFile):
        with open(settingsFile) as json_file:
            data = json.load(json_file)
    else:
        OS = os.system
        if OS == "Linux":
            if platform.processor() == "x86_64":
                autoUpdateURL = "https://proj.ydreams.global/ydreams/apps/projControl_deb"
            else:
                autoUpdateURL = "https://proj.ydreams.global/ydreams/apps/projControl_arm64"
        else:
            autoUpdateURL = "https://proj.ydreams.global/ydreams/apps/projControl.exe"
        data = {
                "projectors" : [
            "192.168.60.30",
            "192.168.60.65",
            "192.168.60.142",
            "192.168.60.247"
        ]
        }
        # Writing to config.json
        saveConfig(data, settingsFile)
    return data

def saveConfig(config, settingsFile):
    # Serializing json
    json_object = json.dumps(config, indent=4)
    # Writing to config.json
    with open(settingsFile, "w") as outfile:
        outfile.write(json_object)
    print(f"Config saved to {settingsFile}")
    return config

def send_comand(command, proj_ip):
    try:
        # Attempt to connect to the host
        with Projector.from_address(proj_ip) as projector:
                projector.authenticate()
                projector.set_power(command.lower())
        print(f"{command} Sent to {proj_ip}")
    except OSError as error:
        print(f"Cant conect to {proj_ip}")

#read Arguments
if len(sys.argv) == 1:
    print("""Possible comands are: 
on
off
on 192.168.0.60.20
""")
    sys.exit(0)
else:
    command = sys.argv[1]
    if len(sys.argv) == 3:
        proj_ip = sys.argv[2]

# Get the current working
# directory (CWD)
try:
    this_file = __file__
except NameError:
    this_file = sys.argv[0]
this_file = os.path.abspath(this_file)
if getattr(sys, 'frozen', False):
    cwd = os.path.dirname(sys.executable)
else:
    cwd = os.path.dirname(this_file)

print("Current working directory:", cwd)

print("Sending Commands")
if len(sys.argv) == 3:
    send_comand(command, proj_ip)
else:
    # Read Config File
    myName = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    settingsFile = os.path.join(cwd, f"{myName}.json")
    print(settingsFile)
    config = readConfig(settingsFile)
    projectores = config["projectors"]

    for proj_ip in projectores:
        send_comand(command, proj_ip)
    print("All Comands Sent")
