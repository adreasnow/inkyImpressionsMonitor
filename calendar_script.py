# from calendar import calendar
from gcsa.google_calendar import GoogleCalendar
from datetime import datetime
from functions import dateDiff
import pandas as pd
from time import time

class calendarClass:
    def __init__(self, frequency=600):
        self.events = pd.DataFrame(columns=['dateTime', 'name', 'timeDiff'])
        self.homeCalendarNames = ['adrea.snow@gmail.com',                                               # Personal
                                    'urq11vov4hsuenio6uvp1fc834@group.calendar.google.com',             # Money
                                    '4usn0hdknrcj86906vfkt9nkhc@group.calendar.google.com',             # Social
                                    '3qk6oen5ohg3b2hf0avdt20amo@group.calendar.google.com'              # Work
                                    ]
        self.uniCalendarNames = ['adrea.snow@monash.edu',                                               # Monash
                                    'c_sj83p0v6hgpp57fc8v7c4d2ic0@group.calendar.google.com',            # Monash Social
                                    'monash.edu_2koojctfhdtakq82jnnf3e656g@group.calendar.google.com',  # Pas People
                                    'c_m8cfd9q3dba7bj2t5anv7qo5ro@group.calendar.google.com',           # TA
                                    'c_vtodh9lppvijucu4sp65tj5iss@group.calendar.google.com'            # Pas Group
                                    ]
        self.homeCalendars = []
        self.uniCalendars = []
        self.groupedEventList = []
        self.frequency = frequency
        self.usageruntime = 0
        self.update()

    def update(self):
        if ((self.usageruntime != 0) and ((time() - self.usageruntime) > self.frequency)) or (self.usageruntime == 0):
            self.groupedEventList = []
            self.events = pd.DataFrame(columns=['dateTime', 'name', 'timeDiff'])
            self.homeCalendars = []
            self.uniCalendars = []
            
            for i in self.homeCalendarNames:
                self.homeCalendars += [GoogleCalendar(i, credentials_path='./auth/credentials.json', token_path='./auth/gmailToken.pickle')]

            for calendar in self.homeCalendars:
                    for event in calendar.get_events(single_events=True, order_by='startTime', ):
                        eventDate = datetime.strptime(str(event.start).split(' ')[0],'%Y-%m-%d').date()
                        toAdd = {'dateTime': eventDate, 'name': event.summary, 'timeDiff': dateDiff(eventDate)}
                        self.events = self.events.append(toAdd, ignore_index=True)


            for i in self.uniCalendarNames:
                self.uniCalendars += [GoogleCalendar(i, credentials_path='./auth/credentials.json', token_path='./auth/monashToken.pickle')]

            for calendar in self.uniCalendars:
                    for event in calendar.get_events(single_events=True, order_by='startTime'):
                        eventDate = datetime.strptime(str(event.start).split(' ')[0],'%Y-%m-%d').date()
                        toAdd = {'dateTime': eventDate, 'name': event.summary, 'timeDiff': dateDiff(eventDate)}
                        self.events = self.events.append(toAdd, ignore_index=True)

            self.events = self.events.sort_values('dateTime')

            prevETA = ''
            tempOutList = []
            for event in self.events.iterrows():
                eta = event[1][2]
                eventName = event[1][1]

                if prevETA == '':
                    prevETA = eta
                    tempOutList += [[eventName, eta]]
                elif prevETA == eta:
                    prevETA = eta
                    tempOutList += [[eventName, eta]]
                else:  
                    prevETA = eta
                    self.groupedEventList += [tempOutList]
                    tempOutList = [[eventName, eta]]

            newGroupedEventList = []
            groupEvents = []
            groupName = ''
            for group in self.groupedEventList:
                for event in group:
                    groupEvents += [event[0]]
                    groupName = event[1]
                newGroupedEventList += [[groupName, groupEvents]]
                groupEvents = []
            self.groupedEventList = newGroupedEventList
            self.usageruntime = time()