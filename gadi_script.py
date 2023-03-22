from time import time
from functions import runbash

class gadiClass:
    def __init__(self, user, frequency=300, reserved_me=960.00):
        self.username = user
        self.frequency = frequency
        self.allocation = 0
        self.reserved_me = reserved_me
        self.userDict = {'as1892': 'Adrea', 'ph0021': 'Peter'}

        # when things were run
        self.usageruntime = 0

        self.grant_project = 0 # <- self.update() 
        self.used_project = 0 # <- self.update() 
        self.reserved_project = 0 # <- self.update() 
        self.avail_project = 0 # <- self.update() 
        self.used_me = 0 # <- self.update() 
        self.avail_me = 0 # <- self.update() 
        self.users = [] # <- self.update() 
        
        self.update() 

    @staticmethod
    def msu2ksu(value, string):
        if string == 'MSU':
            value = float(value) * 1000
        elif string == 'SU':
            value = float(value)/1000
        else:
            value = float(value)
        return(str(round(value, 3)))

    def update(self):
        if ((self.usageruntime != 0) and ((time() - self.usageruntime) > self.frequency)) or (self.usageruntime == 0):
            gadiOutput = runbash(f'ssh {self.username}@gadi.nci.org.au \"nci_account -v\"').splitlines()
            self.grant_project = self.msu2ksu(gadiOutput[2].split()[1], gadiOutput[2].split()[2])
            self.used_project = self.msu2ksu(gadiOutput[3].split()[1], gadiOutput[3].split()[2])
            self.reserved_project = self.msu2ksu(gadiOutput[4].split()[1], gadiOutput[4].split()[2])
            self.avail_project = self.msu2ksu(gadiOutput[5].split()[1], gadiOutput[5].split()[2])
            for i in range(0, len(gadiOutput) - 2):
                if self.username in gadiOutput[i]:
                    self.used_me = self.msu2ksu(gadiOutput[i].split()[1], gadiOutput[i].split()[2])
                    self.avail_me = str(round(float(self.reserved_me) - float(self.used_me), 2))

            self.users = []
            userLineNum = 9999
            for i, val in enumerate(gadiOutput):
                if 'User' in val:
                    userLineNum = i+2
                if i >= userLineNum:
                    try:
                        splitVal = val.split()
                        self.users += [[splitVal[0], self.msu2ksu(splitVal[1], splitVal[2])]]
                    except:
                        break

            self.usageruntime = time()


