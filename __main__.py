from gadi_script import gadiClass
from monarch_script import monarchClass
from functions import wrapString
from warnings import filterwarnings
from PIL import Image, ImageDraw, ImageFont
from time import sleep, time
from datetime import datetime
from os import environ

filterwarnings('ignore')


gadi = gadiClass('as1892', frequency=720)
mon = monarchClass('asnow', frequency=120)
lastRunTime = 0


global hostUser
hostUser = environ['USER'] 
frequency = 240 if hostUser == 'pi' else 20
reInitFreq = 86400 if hostUser == 'pi' else 40

if hostUser == 'pi':
    from inky.auto import auto
    import inky
    display = auto()
    display.set_border(inky.BLACK)
else:
    display = False


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

    # MonARCH #-440
    d.rectangle([(0, 0),(w, 40)], fill='#fa2525') 
    d.rectangle([(0, 40),(w, h)], fill='#fa8282') 
    d.text(((w/2)-50, 4), "MonARCH", font=boldfnt, fill=(0,0,0))
    d.text((15, 50), mon.jobs, font=monofnt, fill=(0,0,0))
    d.line([(0, 0),(w, 0)], fill='#000000', width=4)
    d.line([(0, 40),(w, 40)], fill='#000000', width=3)
    d.text((2*(w/3)+100, 9), f'Storage: {mon.usage} / {mon.quota}', font=fnt, fill=(0,0,0))

    # Gadi
    d.rectangle([(0, h-80),(w, h-40)], fill='#fffc33')
    d.rectangle([(0, h-40),(w, h)], fill='#fffecc')

    gadiValString = f'{gadi.avail_project} KSU free out of {gadi.grant_project} KSU Avail ({gadi.used_project} KSU used)'
    d.text((20, h-75), "Gadi:", font=boldfnt, fill=(0,0,0))
    d.text((100, h-70), gadiValString, font=fnt, fill=(0,0,0))
    d.text((20, h-35), 'Users:', font=fnt2, fill=(0,0,0))

    users = ''
    for user in gadi.users:
        if user[0] in gadi.userDict:
            users += f'{gadi.userDict[user[0]]}: {user[1]} KSU   '
        else:
            users += f'{user[0]}: {user[1]} KSU   '

    d.text((100, h-33), users, font=fnt, fill=(0,0,0))


    # Border
    d.line([(0, 0),(w, 0)], fill='#000000', width=4)
    d.line([(w, 0),(w, h)], fill='#000000', width=4)
    d.line([(0, h),(w, h)], fill='#000000', width=4)
    d.line([(0, 0),(0, h)], fill='#000000', width=4)
    d.line([(0, 40),(w, 40)], fill='#000000', width=3) # bottom of header
    d.line([(0, h-80),(w, h-80)], fill='#000000', width=3) # top of gadi line
    d.line([(0, h-40),(w, h-40)], fill='#000000', width=2) # middle of gadi line

    # Refresh time
    timeString = f'Last Run: {datetime.now().strftime("%a %-I:%M %p")}'
    d.text(((w/3)-300, 9), timeString, font=fnt, fill=(0,0,0))


    img = img.resize((w// 2, h// 2), resample=Image.BICUBIC)
    return img


while True:
    if ((lastRunTime != 0) and ((time() - lastRunTime) > frequency)) or (lastRunTime == 0):
        if hostUser == 'pi':
            display.set_image(drawImg(display).rotate(180))
            display.show()
        else:
            drawImg(display).show()

        lastRunTime = time()

    try: gadi.update()
    except: pass

    try: mon.update()
    except: pass
    
    sleep(1)

