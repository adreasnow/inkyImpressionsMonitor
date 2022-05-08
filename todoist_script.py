from datetime import datetime
from functions import dateDiff
import pandas as pd
from time import time

class todoistClass:
    def __init__(self, APIKey, frequency=310):
        from todoist_api_python.api import TodoistAPI

        self.frequency = frequency
        self.usageruntime = 0
        self.todoistAPI = TodoistAPI(APIKey) 
        self.groupedTaskList = []
        self.orderedTaskList = []
        self.tasks = pd.DataFrame(columns=['dateTime', 'name', 'timeDiff'])
        self.update()

    def update(self):
        if ((self.usageruntime != 0) and ((time() - self.usageruntime) > self.frequency)) or (self.usageruntime == 0):
            try:
                tasks = self.todoistAPI.get_tasks()
            except Exception as error:
                print(error)

            for i in tasks:
                try:
                    taskDate = datetime.strptime(i.due.date, '%Y-%m-%d')
                    taskETA = dateDiff(taskDate.date())
                    taskTitle = i.content
                    toAdd = {'dateTime': taskDate, 'name': taskTitle, 'timeDiff': taskETA}
                    self.tasks = self.tasks.append(toAdd, ignore_index=True)
                except:
                    pass
            
            self.tasks = self.tasks.sort_values('dateTime')

            prevETA = ''
            tempOutList = []
            for task in self.tasks.iterrows():
                eta = task[1][2]
                taskName = task[1][1]
                if prevETA == '':
                    prevETA = eta
                    tempOutList += [[taskName, eta]]
                elif prevETA == eta:
                    prevETA = eta
                    tempOutList += [[taskName, eta]]
                else:  
                    prevETA = eta
                    self.groupedTaskList += [tempOutList]
                    tempOutList = [[taskName, eta]]

            newGroupedTaskList = []
            groupTasks = []
            groupName = ''
            for group in self.groupedTaskList:
                for task in group:
                    groupTasks += [task[0]]
                    groupName = task[1]
                newGroupedTaskList += [[groupName, groupTasks]]
                groupTasks = []
            self.groupedTaskList = newGroupedTaskList
            self.usageruntime = time()
