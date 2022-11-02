import subprocess
from datetime import datetime

def runbash(command):
    output = subprocess.run(command, stdout=subprocess.PIPE, shell=True).stdout.strip()
    if output != "":
        return(output.decode("utf-8"))

def wrapString(inString, chars):
    if len(inString) > chars:
        outString = inString[:chars-3]
        if len(inString) > chars-3:
            outString += '...'
        return outString
    else:
        return inString
