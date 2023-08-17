#!/usr/bin/python3

import argparse
import json
import pprint
import sys
from tkinter import *
from tkinter import ttk

import yaml
from pythonosc import udp_client
from targets import *

# Globals
rootWindow = Tk()
currentCue = StringVar()
currentCue.set('Cue Playing:')


def fire_cue(cueNumber):
    print("Firing Cue Number {}".format(cueNumber))
    for target in cueInfo["cues"][cueNumber]["targets"]:
        for param in cueInfo["cues"][cueNumber]["targets"][target]["setparams"]:
            print("param: {}".format(param))
            targets[target].setParam(param)

def main():

    rootWindow.title('Hello World!!!')
    mainFrame = ttk.Frame(rootWindow, padding="3 3 12 12")
    mainFrame.grid(column=0, row=0, sticky=(N, W, E, S))
    mainFrame.columnconfigure(0, weight=1)
    mainFrame.rowconfigure(0, weight=1)

    Button(mainFrame, text="1.1.00 - assign", command=(lambda n="1.1.00": fire_cue(n))).grid(column=0, row=0, sticky=(W, E))
    Button(mainFrame, text="1.1.99 - un-assign", command=(lambda n="1.1.99": fire_cue(n))).grid(column=1, row=0, sticky=(W, E))
    Button(mainFrame, text="EXIT", command=sys.exit).grid(column=2, row=0, sticky=(W, E))

    Label(mainFrame, textvariable=currentCue).grid(column=1, columnspan=2, row=1, sticky=(W, E) )
    for child in mainFrame.winfo_children(): child.grid_configure(padx=5, pady=5)

    rootWindow.mainloop()


def loadConfigFiles():
    global showInfo
    showInfo = yaml.safe_load( open( args.show_file ) )
    global cueInfo
    cueInfo = json.load( open( args.cue_file ) )
    global targetInfo
    targetInfo = yaml.safe_load( open( args.target_file ) )
    return True

def configureTargets():
    global targets
    targets=dict()
    targets['AudioConsole01'] = OSC_M32.OSC_M32(targetInfo['AudioConsole01'])
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--show_file", type=str, default="./show.cfg",
                        help="The name of the show configuration file")
    parser.add_argument("--cue_file", type=str, default="./cues.cfg",
                        help="The name of the cue file")
    parser.add_argument("--target_file", type=str, default="./targets.cfg",
                        help="target confoguration file")
    args = parser.parse_args()

    # Load Configuration Files
#    try:
    assert loadConfigFiles() == True
#    except:
#        print("Something went wrong when loading the configuration.  Quitting!")
#        quit()

    #print( yaml.safe_dump( targetInfo ) )

    # Configure Targets
    try:
        assert configureTargets() == True
    except:
        print("Something went wrong while configuring targets.  Quitting!!")
        quit()

    main()

