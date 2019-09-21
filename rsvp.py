#! python3
# Python script for RSVP, "Really Simple Video Place"
import sys
import os
import subprocess
from concurrent.futures import ThreadPoolExecutor as Pool
import urllib.request
import pytuya
import time
import itertools
import tkinter as tk
from PIL import Image, ImageTk
import tkinter.font as tkFont
import tkinter.messagebox as mB

# this function tries several times to turn on or off the WiFi Sockets
def set_state(device,state):
    for i in itertools.repeat(None,5):
        try:
            if device.status()['dps']['1'] == state:
                return True
            device.set_status(state)
        except:
            time.sleep(0.1)
    return True

# function called to turn off the lighting and kill the other tasks
def onExit(future):
    if future.exception() is not None:
        print("got exception: %s" % future.exception())
    else:
        print("process returned %d" % future.result())

    stopLites(d1,d2,d3)
# kill the powerpoint viewer
    os.system("taskkill /f /im PPTVIEW.EXE")
# kill the browser
    os.system("taskkill /f /im chrome.exe")
    print("OBS Exited")

def startLites(d1,d2,d3):
   set_state(d1,True)
   set_state(d2,True)
   set_state(d3,True)

def stopLites(d1,d2,d3):
   set_state(d1,False)
   set_state(d2,False)
   set_state(d3,False)

def hello():
#	print("Single Click, Button-1")
	print(v.get())
	startOBS(v.get())
	root.destroy()

def help():
	print("Help is on the way")
	htext = """* Select the first option if you want to use a PowerPoint presentation in your video.

* Select the second option if you want to use a browser window in your video.

*Select the third option (Camera only) if you don't need either, thanks."""
	mB.showinfo("Help",htext)

# these are our ids for our sockets, you need to insert your own.
d1 = pytuya.OutletDevice('83240602840d8e9cc884', '172.20.33.26' , '3bce7d09ea1b896e')
d2 = pytuya.OutletDevice('24876438840d8e9cc8db', '172.20.33.27', 'cb6de4ad75170514')
d3 = pytuya.OutletDevice('83240602cc50e3d502d7', '172.20.33.28', '287a1c6eb20d5d5f')

def startOBS(whichone):
    print("Starting OBS")

    startLites(d1,d2,d3)

    pool = Pool(max_workers=1)
# whichone is which option selected, 1 for PowerPoint, 2 for Browser
    if whichone == 1:
        f = pool.submit(subprocess.call, ["C:\\Program Files\\obs-studio\\bin\\64bit\\obs64.exe", "--profile", "RSVP", "--collection", "RSVP", "--scene", "Camera", "--studio-mode"], cwd = "C:\\Program Files\\obs-studio\\bin\\64bit")
    elif whichone == 2:
        f = pool.submit(subprocess.call, ["C:\\Program Files\\obs-studio\\bin\\64bit\\obs64.exe"," --profile", "RSVP", "--collection", "BrowserScene", "--scene", "Camera", "--studio-mode"], cwd = "C:\\Program Files\\obs-studio\\bin\\64bit")
    else:
        f = pool.submit(subprocess.call, ["C:\\Program Files\\obs-studio\\bin\\64bit\\obs64.exe", "--profile", "RSVP", "--collection", "RSVP", "--scene", "Camera", "--studio-mode"], cwd = "C:\\Program Files\\obs-studio\\bin\\64bit")

    f.add_done_callback(onExit)
    pool.shutdown(wait=False)

    if whichone == 1:
        os.startfile (r"C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Microsoft PowerPoint Viewer .lnk")
    elif whichone == 2:
        os.startfile (r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe")
#	subprocess.Popen([r"/usr/bin/google-chrome-stable %U" , "--app='data:text/html,<html><body><script>window.moveTo(580,240);window.resizeTo(1920,1080);</script></body></html>'"])

root = tk.Tk()
cFont = tkFont.Font(family="Arial", size=24)

v = tk.IntVar()
v.set(1) # initializes the first choice

tk.Label(root,text="""Click on an option\nthen click Start""", justify=tk.LEFT,padx=20,font=cFont).pack()
root.title("RSVP Options")

image = Image.open("chrome.jpeg")
out = image.resize((64, 64))
myImage = ImageTk.PhotoImage(out)
impp = Image.open("PowerPoint.png")
outpp = impp.resize((64,64))
myimpp = ImageTk.PhotoImage(outpp)
rimpp = Image.open("rsvp.png")
routpp = rimpp.resize((64,64))
rmimpp = ImageTk.PhotoImage(routpp)
# radio buttons here
tk.Radiobutton(root,text="RSVP with PowerPoint",padx=20,variable=v,value=1,image=myimpp,compound=tk.LEFT,font=cFont).pack(anchor=tk.W)
tk.Radiobutton(root,text="RSVP with Browser",padx=20,variable=v,value=2,image=myImage,compound=tk.LEFT,font=cFont).pack(anchor=tk.W)
tk.Radiobutton(root,text="RSVP Camera Only",padx=20,variable=v,value=3,image=rmimpp,compound=tk.LEFT,font=cFont).pack(anchor=tk.W)
#other buttons here
helpButton  = tk.Button(root,font=cFont,text="Help",command=help).pack(anchor=tk.W,side=tk.LEFT)
startButton = tk.Button(root,font=cFont,text="Start",command=hello).pack(anchor=tk.W,side=tk.RIGHT)
# startbutton calls "hello" to start the program
# helpbutton brings up the help windows.
root.mainloop()
print("Here we go!")
print("Completely Done")
