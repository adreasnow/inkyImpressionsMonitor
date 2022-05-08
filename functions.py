import subprocess
from datetime import datetime

def runbash(command):
    output = subprocess.run(command, stdout=subprocess.PIPE, shell=True).stdout.strip()
    if output != "":
        return(output.decode("utf-8"))

def dateDiff(date):
    today = datetime.today().date()
    delta = (date - today).days
    if delta == 0:
        timeOut = 'Today'
    elif delta == 1:
        timeOut = 'Tomorrow'
    elif delta < 7:
        timeOut = f'{delta} Days'
    else:
        timeOut = f'{round(delta / 7)} Weeks'
        if round(delta / 7) == 1:
            timeOut = f'1 Week'
    return(timeOut)

def wrapString(inString, chars):
    if len(inString) > chars:
        outString = inString[:chars-3]
        if len(inString) > chars-3:
            outString += '...'
        return outString
    else:
        return inString
