from time import time
from functions import runbash

class monarchClass:
    def __init__(self, user, frequency=60):
        self.username = user
        self.frequency = frequency

        # when things were run
        self.usageruntime = 0
        self.jobs = {}
        self.update() 

    def time2str(self, timestr):
        outstr = ' '
        splithyphen = timestr.split('-')
        outstr += f'{splithyphen[0]}D-' if len(splithyphen) > 1 else '   '
        splitcolon = splithyphen[-1].split(':')
        if len(splitcolon) == 3:
            outstr += f'{splitcolon[-3]:>2}H-{splitcolon[-2]:>2}M'
        elif len(splitcolon) == 2:
            outstr += f'    {splitcolon[-2]:>2}M'
        elif len(splitcolon) == 1:
            outstr += f'   {splitcolon[-1]:>2}S'
        return(outstr)

    def time2strShort(self, timestr):
        splithyphen = timestr.split('-')
        splitcolon = timestr.split(':')
        # print(splithyphen)
        if len(splithyphen) > 1:
            outstr = f' {splithyphen[0]}D '
        elif len(splitcolon) == 3:
            outstr = f'{splitcolon[0]:>2}H '
        elif len(splitcolon) == 2:
            outstr = f'{splitcolon[0]:>2}M '
        return(outstr)

    def update(self):
        if ((self.usageruntime != 0) and ((time() - self.usageruntime) > self.frequency)) or (self.usageruntime == 0):
            tooManyJobs = False
            squeueString = '%.18i %10P %30j %.8T %.12L %.10l %.4m %.4C %.8q %.5R'
            monOutput = runbash(f'ssh {self.username}@monarch.erc.monash.edu \"/opt/slurm-latest/bin/squeue -o\'{squeueString}\' -u {self.username} --sort=-T,j\"').splitlines()
            m3Output = runbash(f'ssh {self.username}@m3.massive.org.au \"/opt/slurm-latest/bin/squeue -o\'{squeueString}\' -u {self.username} --sort=-T,j\"').splitlines()
            self.jobs = 'Job ID  Part              Job Name                 Status       Time Left       Mem   CPU  QOS    Node(s)\n'
            self.jobs += '-----------------------------------------------------------------------------------------------------------\n'
            runningList1 = [i for i in monOutput[1:] if 'RUNNING' in i]
            runningList2 = [i for i in m3Output[1:] if 'RUNNING' in i]
            queuedList1 = [i for i in monOutput[1:] if 'PENDING' in i]
            queuedList2 = [i for i in m3Output[1:] if 'PENDING' in i]
            clusterList = runningList1 + runningList2 + queuedList1 + queuedList2

            for i, val in enumerate(clusterList):
                if i < 30:
                    self.jobs += ' '.join([val[11:69], self.time2str(val[70:94].split()[0]),"of", self.time2strShort(val[70:94].split()[1]), val[94:]])
                    self.jobs += '\n'
                else:
                    self.jobs += '...' if tooManyJobs == False else ''

            monOutput = runbash(f'ssh {self.username}@monarch.erc.monash.edu \"cd ~/p2015120004 && /bin/lfs quota -h -g p2015120004 .\"').splitlines()
            self.usage = monOutput[2].split()[1]
            self.quota = monOutput[2].split()[2]

            self.usageruntime = time()
