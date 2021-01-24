# Neat colors - taken from stackoverflow
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Try to import pyscreenshot first - I use it and PIL doesnt work on
# Linux devices
try:
    import pyscreenshot as ImageGrab
# Try to import PIL if pyscreenshot not installed
except ImportError:
    print(bcolors.FAIL+"pyscreenshot is not installed! attempting to use" \
          " PIL instead."+bcolors.ENDC)
    from PIL import ImageGrab
# pyUserInput - can be changed out for any other keyboard//mouse controlling
# Libs
from pymouse import PyMouse
from pykeyboard import PyKeyboard
# time for sleep, datetime for printing,
# keyboard to check if key press (might be able to be done w/ pyuserinput?)
# json for loading configs (maybe change?)
import time, datetime, keyboard, json

# Example Switch // Case function - Mainly from stackoverflow
def config(confVar):
    with open('config.json', 'r') as openFile:
        confFile = json.load(openFile)
    # switch not needed but ensures it does not try to get invalid args
    switcher = {
        "speed": confFile.get('speed'),
        "loopmax" : confFile.get('loopmax'),
        "xpos" : confFile.get('xpos'),
        "ypos" : confFile.get('ypos'),
        "restartXY" : confFile.get('restartXY'),
        "refreshXY" : confFile.get('refreshXY')
    }
    # return false if confVar not in switcher -
    # might want to edit if a setting is bool
    confVal = switcher.get(confVar, False)
    return confVal


m = PyMouse()
k = PyKeyboard()

# just leftclick and sleep lol
# Not sure if m.click requires x,y but better safe than sorry
def leftClick():
    x,y=m.position()
    m.click(x,y,1)
    time.sleep(.1/speed)

# set mouse pos - function only for readability
def mousePos(x,y):
    m.move(x,y)
    time.sleep(.1/speed)

def restartGame(pos):
    #location of first menu
    mousePos(pos[0],pos[1])
    leftClick()

# re-type the URL just in case it leaves the page
def refreshSite(pos):
    # Expects pos to be formatted as [x,y]
    # Input vars could be set to x,y, but it works for now
    mousePos(pos[0],pos[1])
    leftClick()
    time.sleep(.1/speed)
    k.type_string('')
    time.sleep(.5/speed)
    keyboard.press('enter')
    time.sleep(.25/speed)

def main():
    # set speed to global here, else it'll need to
    # be set global outside of function //
    # not the best way to do it, but it works lolol
    global speed
    # get vars from config
    speed = float(config("speed"))
    xpo=sorted(config("xpos"))
    ypo=sorted(config("ypos"))
    refreshSitePos=config('refreshXY')
    restartGamePos=config('restartXY')
    loopmax = int(config("loopmax"))
    # reverse ypo so it goes top-down
    ypo.reverse()
    # reversing xpo will make it go right-left
    #xpo.reverse()
    loopcount=0
    refreshcount=0
    #background colors
    colors=[(198,217,241),(54,57,63)]
    while True:
        loopcount+=1
        print(bcolors.HEADER + bcolors.UNDERLINE + "Loop number #%s of Refresh #%s"%(loopcount,refreshcount) + bcolors.ENDC)
        # Check if we've clicked in a grid loop enough
        if loopcount == loopmax:
            refreshSite(refreshSitePos)
            refreshcount+=1
            print(bcolors.BOLD + "Refreshed site. Refresh #%s"%(refreshcount) + bcolors.ENDC)
            # only use of datetime; might be better to
            # import datetime.datetime
            now=datetime.datetime.now()
            current_time=now.strftime("%H:%M:%S")
            print("Current time is: %s"%(current_time))
            time.sleep(6.5/speed)
            loopcount=0
        restartGame(restartGamePos)
        # Check if user wants to exit
        if keyboard.is_pressed('q'):
            print(bcolors.FAIL + 'QUITTING. PRESS CTRL+C IF PROGRAM DOES NOT EXIT.' + bcolors.ENDC)
            quit()
            print("Quit failure. Attempting System.Exit().")
            exit()
            # at this point we giving up lol
            import sys
            sys.exit(0)
            print("Exit failure. Please press CTRL+C or kill the python task.")
            time.sleep(100000)
        # Check if user wants to pause
        if keyboard.is_pressed('p'):
            print(bcolors.OKBLUE + 'PAUSED.' + bcolors.ENDC)
            pausevar=input("Press enter to resume: ")
        time.sleep(0.5/speed)
        im=ImageGrab.grab()
        print(bcolors.OKGREEN + "Grabbed Screen." + bcolors.ENDC)
        for xpos in xpo:
            if im.getpixel((xpos,ypo[0])) not in colors:
                print(bcolors.OKCYAN + "Column %s contains cells"%(xpos)
                      + bcolors.ENDC)
                for ypos in ypo:
                    #print("Checking at X%s Y%s"%(xpos,ypos))
                    if im.getpixel((xpos,ypos)) not in colors:
                        # both mousePos and leftClick move the mouse -
                        # might want to change but it works for now
                        mousePos(xpos,ypos)
                        leftClick()
                        time.sleep(.05/speed)
                        print("Clicked at X%s Y%s"%(xpos,ypos))
                    else:
                        # when it's reached the top
                        print(bcolors.WARNING + "Breaking at Y%s"%(ypos)
                              + bcolors.ENDC)
                        break
            else:
                # when it's gone as far right as it could
                print(bcolors.FAIL + "Breaking at X%s"%(xpos) + bcolors.ENDC)
                break

# dont do anything if not main
if __name__ == '__main__':
    main()
