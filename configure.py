import json

def confirm():
    print("")

# custom function
def rowPrint(xrow=-1,yrow=-1,xpos=-1,ypos=-1,width=9,height=9):
    rows = [["O"]*width for _ in range(height)]
    for list in rows:
        if yrow != -1:
            list[yrow]="X"
    if xrow != -1:
        rows[xrow] = ["X"]*width
    if ypos != -1:
        n=rows[ypos]
        if xpos != -1:
           n[xpos]="X"
    for list in rows:
        printable=""
        for str in list:
            printable+=" "+str
        print(printable)
#rowPrint(1,2,7,6)

def saveJson(currentJson):
    configFile=open('config.json','w')
    configFile.write(json.dumps(currentJson))
    configFile.close()
    print("Saved settings: ")
    print(currentJson)
    print("Exiting.")
    quit()
    import sys
    sys.exit(0)
    print("If you are seeing this, please press CTRL+C")
    import time
    time.sleep(100000)

def confSpeed():
    print("------------------------")
    try:
        return float(input("What speed should I click at? (Default: 1) "))
    except ValueError:
        print("You have to put a number greater than zero! Any other characters will not work (!#$&$*@), though you may put fractions (ex: .5, 1.5, 2.3)")
        return float(input("What speed should I click at? (Default: 1) "))

def confLoopMax():
    print("------------------------")
    try:
        return int(input("How many times should I scan the screen for planets before refreshing?: (default: 50) "))
    except ValueError:
        print("You have to put a number greater than zero! Any other characters will not work (!#$&$*@)")
        return int(input("How many times should I scan the screen for planets before refreshing?: (default: 50) "))


def confxposs():
    import keyboard
    from pymouse import PyMouse
    m=PyMouse()
    print("------------------------")
    rowPrint(8,-1,-1,-1)
    print("We will now select the X Positions of the planets.")
    print("Please have your browser ready with the site open, and it is recommended that you maximize the window.")
    input("Press enter when ready: ")
    xpossl=[]
    for x in range(9):
        print("------------------------")
        rowPrint(-1,-1,8,x)
        print("Please press W when you have your mouse hovered over this planet.")
        keyboard.wait('w')
        xpossl.append(m.position()[0])
    return xpossl

def confyposs():
    import keyboard
    from pymouse import PyMouse
    m=PyMouse()
    print("------------------------")
    rowPrint(-1,0,-1,-1)
    print("We will now select the Y Positions of the planets.")
    print("Please have your browser ready with the site open, and it is recommended that you maximize the window.")
    input("Press enter when ready: ")
    ypossl=[]
    for y in range(9):
        print("------------------------")
        rowPrint(-1,-1,y,0)
        print("Please press W when you have your mouse hovered over this planet.")
        keyboard.wait('w')
        ypossl.append(m.position()[1])
    return ypossl

def confRestartXY():
    import keyboard
    from pymouse import PyMouse
    m=PyMouse()
    print("------------------------")
    print("We will now select the position of the restart button.")
    print("Please have your browser ready with the site open, and it is recommended that you maximize the window.")
    print("For this step, you may have to complete a game of planet popper to correctly position the mouse.")
    input("Press enter when ready: ")
    print("Please press W when you have your mouse hovered over it.")
    keyboard.wait('w')
    rxyp=m.position()
    return [rxyp[0],rxyp[1]]

def confRefreshXY():
    import keyboard
    from pymouse import PyMouse
    m=PyMouse()
    print("------------------------")
    print("We will now select the position of the URL bar.")
    print("Please have your browser ready")
    print("For this step, you will hover your mouse over the URL bar.")
    print("This is to refresh the website every X loops to ensure any bugs do not occur.")
    input("Press enter when ready: ")
    print("Please press W when you have your mouse hovered over it.")
    keyboard.wait('w')
    rxyp=m.position()
    return [rxyp[0],rxyp[1]]

def retry(currentJson):
    done=0
    while done==0:
        print("------------------------")
        print("Current Settings:")
        print(currentJson)
        print("------------------------")
        print("To redo configuration, type retry.")
        print("To edit the speed, type speed.")
        print("To edit the loopmax, type loopmax.")
        print("To edit the xposs, type xposs.")
        print("To edit the yposs, type yposs.")
        print("To edit the RestartXY, type RestartXY.")
        print("To edit the RefreshXY, type RefreshXY.")
        print("Type Cancel to cancel.")
        wrongSetting=str(input("Selection: ")).lower()
        if wrongSetting == "speed":
            newspeed=confSpeed()
            currentJson['speed']=newspeed
        elif wrongSetting == "loopmax":
            newmax=confLoopMax()
            currentJson['loopmax']=newmax
        elif wrongSetting == "xposs":
            newxposs=confxposs()
            currentJson['xposs']=newxposs
        elif wrongSetting == "yposs":
            newyposs=confyposs()
            currentJson['yposs']=newyposs
        elif wrongSetting == "restartxy":
            newrestxy=confRestartXY() 
            currentJson['restartXY']=newrestxy
        elif wrongSetting == "refreshxy":
            newrefrxy=confRefreshXY()
            currentJson['refreshXY']=newrefrxy
        elif wrongSetting=="cancel":
            done=1
        else:
            print("Invalid selection.")
        if done != 1:
            print("Continue editing? Y/N: ")
            continuevar=str(input('')).lower()
            if continuevar == "n":
                done=1
    return currentJson

def checkConfirm(currentJson):
    print("------------------------")
    print("Current Settings:")
    print(currentJson)
    print("------------------------")
    print("Are these settings correct?")
    confirm=str(input("Type Y/Yes or N/No to select: ")).lower()
    confirmed=['y','ye','yes']
    nconfirmed=['n','no']
    status=3
    while status == 3:
        if confirm in confirmed:
            status=1
        elif confirm in nconfirmed:
            status=2
        else:
            confirm=str(input("Type Y/Yes or N/No to select: ")).lower()
            status=3
    if status==1:
         print("confirmed")
    if status==2:
         currentJson=retry(currentJson)
    return currentJson

def configure(configFile):
    try:
        confJson=json.loads(configFile.read())
        print("Loaded current config")
        #print(confJson)
        cmode=-1
    except ValueError:
        print("Config file not correctly loaded. Creating...")
        cmode=0
    emptyConfig={"speed" : 0,
                  "loopmax" : 0,
                  "xposs" : [],
                  "yposs" : [],
                  "restartXY" : [],
                  "refreshXY" : []}
    print("Entering mode %s"%(cmode))
    if cmode == 0:
        configFile.write(json.dumps(emptyConfig))
        confSpeedr=confSpeed()
        confLoopMaxrow=confLoopMax()
        currentSettings={"speed" : confSpeedr,
                         "loopmax" : confLoopMaxrow,
                         "xposs" : confxposs(),
                         "yposs" : confyposs(),
                         "restartXY" : confRestartXY(),
                         "refreshXY" : confRefreshXY()}
        print("Current settings: %s"%(currentSettings))
        print("Is this correct?")
        new=checkConfirm(currentSettings)
        saveJson(new)
    if cmode == -1:
        new=retry(confJson)
        saveJson(new)

if __name__ == '__main__':
    try:
        configFile=open('config.json','r+')
        configure(configFile)
    except IOError:
        configFile=open('config.json','w+')
        configure(configFile)
