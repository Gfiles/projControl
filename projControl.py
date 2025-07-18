#!/usr/bin/python3
"""
{
    "projectors" : [
        "192.168.60.117",
        "192.168.60.114",
        "192.168.60.116",
        "192.168.60.121",
        "192.168.60.10"
    ] 
}
"""
import json
import os
import sys

from pypjlink import Projector #pip install pypjlink2

def readConfig():
    settingsFile = os.path.join(cwd, "config.json")
    with open(settingsFile) as json_file:
        data = json.load(json_file)
    return data

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

# Read Config File
config = readConfig()
projectores = config["projectors"]

print("Send Commands")
for projIP in projectores:
    try:        
        with Projector.from_address(projIP) as projector:
            projector.authenticate()
            projector.set_power('off')
    except Exception as error:
        print(f"{error} with {projIP}")
print("All Comands Sent")