from todoist_script import todoistClass
from calendar_script import calendarClass
from gadi_script import gadiClass
from monarch_script import monarchClass
from functions import wrapString
from warnings import filterwarnings
from PIL import Image, ImageDraw, ImageFont
from time import sleep, time
from os import environ

filterwarnings('ignore')


todoist = todoistClass('054bed5f786a1efe7d6c54a900d1a72e48b74308', frequency=360)
gCal = calendarClass(frequency=360)
gadi = gadiClass('as1892', frequency=720)
mon = monarchClass('asnow', frequency=120)
lastRunTime = 0

global hostUser
hostUser = environ['USER'] 
frequency = 240 if hostUser == 'pi' else 20

if hostUser == 'pi':
    from inky.auto import auto
    import inky
    display = auto()
    display.set_border(inky.BLACK)
else:
    display = False



def eventList(eventList):
    dayString = ''
    dayName = ''
    maxEventLen = 34
    maxEventCount = 16
    for day in eventList:
        count = 1
        dayString += f'{wrapString(day[1][0], maxEventLen)}\n'
        dayName += f'{day[0]}:\n'

        try:
            for event in day[1][1:]:
                dayString += f'{wrapString(event, maxEventLen)}\n'
                dayName += '\n'
                count += 1
        except:
            pass
        dayStringCulled = '\n'.join(dayString.split('\n')[:maxEventCount-1])
        dayNameCulled = '\n'.join(dayName.split('\n')[:maxEventCount-1])
    return dayNameCulled, dayStringCulled

def drawImg(display):
    global hostUser
    if hostUser == 'pi':
        w, h = display.resolution
        w = w*2
        h = h*2
    else:
        w = 600*2
        h = 448*2

    fnt = ImageFont.truetype('fonts/Roboto-Regular.ttf', 22)
    fnt2 = ImageFont.truetype('fonts/Roboto-Regular.ttf', 24)
    boldfnt = ImageFont.truetype('fonts/Roboto-Bold.ttf', 30)
    monofnt = ImageFont.truetype('fonts/RobotoMono-Regular.ttf', 18)
    img  = Image.new(mode="RGB", size=(w, h), color=(255,255,255))
    d = ImageDraw.Draw(img)

    # MonARCH
    d.rectangle([(0, 440),(w, 480)], fill='#fffb00')
    d.rectangle([(0, 480),(w, h)], fill='#fffbc2')
    d.text(((w/2)-50, 444), "MonARCH", font=boldfnt, fill=(0,0,0))
    d.text((15, 490), mon.jobs, font=monofnt, fill=(0,0,0))
    d.line([(0, 440),(w, 440)], fill='#000000', width=4)
    d.line([(0, 480),(w, 480)], fill='#000000', width=3)
    d.text((2*(w/3)+100, 449), f'Storage: {mon.usage} / {mon.quota}', font=fnt, fill=(0,0,0))

    # Calendar
    d.rectangle([(0, 0),(2*(w/5), 40)], fill='#0000ff')
    d.rectangle([(0, 40),(2*(w/5), 440)], fill='#b8b8ff')
    d.text((170, 3), "Calendar", font=boldfnt, fill=(0,0,0))

    dayName, dayString =  eventList(gCal.groupedEventList)
    d.text((15, 50), dayName, font=fnt, fill=(0,0,0))
    d.text((135, 50), dayString, font=fnt, fill=(0,0,0))
    
    # Todoist
    d.rectangle([(2*(w/5), 0),(4*(w/5), 40)], fill='#ff0000')
    d.rectangle([(2*(w/5), 40),(4*(w/5), 440)], fill='#ffd4d4')
    d.text((590, 3), "To-do & Milestones", font=boldfnt, fill=(0,0,0))

    dayName, dayString =  eventList(todoist.groupedTaskList)
    d.text((15+(2*(w/5)), 50), dayName, font=fnt, fill=(0,0,0))
    d.text((135+(2*(w/5)), 50), dayString, font=fnt, fill=(0,0,0))

    # Gadi
    d.rectangle([(4*(w/5), 0),(w, 40)], fill='#00ff00')
    d.rectangle([(4*(w/5), 40),(w, 440)], fill='#c2ffc2')
    d.text((1050, 3), "Gadi", font=boldfnt, fill=(0,0,0))

    gadiNameString = 'Grant:\nUsed:\nAvail:'
    gadiValString = f'{gadi.grant_project}\n{gadi.used_project}\n{gadi.avail_project}'
    gadiMSUString = f'KSU\nKSU\nKSU'

    d.text((80+(4*(w/5)), 50), 'Project', font=fnt2, fill=(0,0,0))
    d.line([(50+(4*(w/5)), 85),(180+(4*(w/5)), 85)], fill='#000000', width=2)
    d.text((15+(4*(w/5)), 100), gadiNameString, font=fnt, fill=(0,0,0))
    d.text((110+(4*(w/5)), 100), gadiValString, font=fnt, fill=(0,0,0))
    d.text((180+(4*(w/5)), 100), gadiMSUString, font=fnt, fill=(0,0,0))

    d.text((85+(4*(w/5)), 195), 'Users', font=fnt2, fill=(0,0,0))
    d.line([(50+(4*(w/5)), 230),(180+(4*(w/5)), 230)], fill='#000000', width=2)


    users = ''
    userUsage = ''
    KSUList = ''
    for user in gadi.users:
        users += f'{user[0]}\n'
        userUsage += f'{user[1]}\n'
        KSUList += 'KSU\n'

    d.text((15+(4*(w/5)), 240), users, font=fnt, fill=(0,0,0))
    d.text((110+(4*(w/5)), 240), userUsage, font=fnt, fill=(0,0,0))
    d.text((180+(4*(w/5)), 240), KSUList, font=fnt, fill=(0,0,0))

    # Border
    d.line([(0, 0),(w, 0)], fill='#000000', width=4)
    d.line([(w, 0),(w, h)], fill='#000000', width=4)
    d.line([(0, h),(w, h)], fill='#000000', width=4)
    d.line([(0, 0),(0, h)], fill='#000000', width=4)
    d.line([(0, 40),(w, 40)], fill='#000000', width=3) # bottom of header
    d.line([(4*(w/5), 0),(4*(w/5), 440)], fill='#000000', width=3) # todo/gadi
    d.line([(2*(w/5), 0),(2*(w/5), 440)], fill='#000000', width=3) # cal/todo


    img = img.resize((w// 2, h// 2), resample=Image.BICUBIC)
    return img


while True:
    if ((lastRunTime != 0) and ((time() - lastRunTime) > frequency)) or (lastRunTime == 0):
        if hostUser == 'pi':
            display.set_image(drawImg(display))
            display.show()
        else:
            drawImg(display).show()

        lastRunTime = time()

        # updates
        try:
            gCal.update()
        except:
            pass

        try:
            gadi.update()
        except:
            pass

        try:    
            mon.update()
        except:
            pass
        try:
            todoist.update()
        except:
            pass
    sleep(1)

