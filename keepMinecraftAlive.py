#filename: keepMinecraftAlive.py
#author: Seamus Finlayson
#date: 2022-12-26

#include libraries
import pyautogui
import time
import keyboard
import pygetwindow
import random

#seed random number generation
random.seed()

#debug only
# while True:
#     windowTitle = str(pygetwindow.getActiveWindowTitle())
#     print(windowTitle)
#     if windowTitle.startswith("Minecraft ") and windowTitle.count("Multiplayer"):
#         print("good window")
#     else :
#         print("bad window")
#     time.sleep(1)

#startup
print("*************************************************************")
print("Minecrat AFK Mouse Clicker")
print("Places and breaks a torch every 5 seconds through automated mouse clicks.")
print("In Minecraft equip a torch and face a wall.")
print("Press 'ctrl + i' to turn clicking on.")
print("Press 'ctrl + u' to turn clicking off. Clicking will automatically turn off when you jump, enter your inventory, or enter the game menu.")
print("Press 'ctrl + o' (the letter) to terminate this program.")
print("Key presses are only registered when Minecraft is the active window and you are playing Multiplayer.")
print("*************************************************************")

#initialize timer for clicking frequency
clickingTimer = time.time()

#variable to lock maximum polling frequency at 20Hz
pollFrequencyTimer = time.time()

#variable for sending an AFK message every 15 minutes
afkMessageTimer = time.time()

#place and break torch
def doTorchAction():
        
    print("doing torch action")
    pyautogui.click(button='right') #place torch
    pyautogui.click() #break torch

#variable for tracking which message to send
NUMBER_OF_MESSAGES = 3
messageNumberTracker = random.randint(0, NUMBER_OF_MESSAGES)

#send a random afk message
def sendAfkMessage(messageNumber):

    #tell user a message has been sent in terminal
    print("message sent to chat")

    #open chat
    pyautogui.write('t')

    #1 in 10 chance of sending message in the Enchantment Table's glyphs
    sendWeirdMessage = random.randint(0,9)

    #type message
    if (not sendWeirdMessage) and (messageNumber == 1):
        pyautogui.write("/tellraw @a {\"text\":\"Erebus Holdings: Proud supplier of equipment for minors who go deep!\", \"color\":\"blue\",\"font\":\"alt\"}")
    else:
        match messageNumber:
            case 0:
                pyautogui.write("/tellraw @a {\"text\":\"Need a diamond? Or three? Try the Erebus Holdings Maze! The entrance is at spawn! (-71, 73, 4)\", \"color\":\"blue\"}")
            case 1:
                pyautogui.write("/tellraw @a {\"text\":\"Erebus Holdings: Proud supplier of equipment for miners who go deep!\", \"color\":\"blue\"}")
            case 2:
                pyautogui.write("/tellraw @a {\"text\":\"Low on iron or gunpowder? Erebus Holdings has you covered! Come to our fully equipped workshop!\", \"color\":\"blue\"}")
                pyautogui.press('enter')
                pyautogui.write('t')
                pyautogui.write("/tellraw @a {\"text\":\"It is supplied by our iron farm and connected to our mob farm. Aquatic entrance at (-426, 62, 130) Ground entrance at (513, 122, 131)\", \"color\":\"blue\"}")
            case 3:
                pyautogui.write("/tellraw @a {\"text\":\"Want a fun AFK program? Get this one at https://github.com/sfinlayson126/Minecraft-AFK-Mouse-Clicker\", \"color\":\"blue\"}")
            
    #send message
    pyautogui.press('enter')

    #update message number tracker
    if messageNumber < NUMBER_OF_MESSAGES:
        messageNumber += 1
    else:
        messageNumber = 0

    return messageNumber

#state machine setup and state meanings
#state = 0 => inactive state, do nothing
INACTIVE = 0
#state = 1 => clicking state, placing torches every 5 seconds
CLICKING = 1
#state = 2 => typing state, ignore certain deactivating keys for state 1 while user is typing
TYPING = 2
#set initial state to inactive
state = INACTIVE
#indicate state in terminal
print("inactive")

#flag to exit program
quit = False

#main loop
while not quit:

    #check time at which polling cycle starts
    pollFrequencyTimer = time.time()

    #check if minecraft in multiplayer is the active window
    windowTitle = str(pygetwindow.getActiveWindowTitle())
    if windowTitle.startswith("Minecraft ") and windowTitle.count("Multiplayer"):

        #detect exit key pressed
        if keyboard.is_pressed('ctrl+o'):
            quit = True

        #turn clicking off
        if keyboard.is_pressed('ctrl+u'):

            #indicate state change in terminal
            print("inactive")

            #change state
            state = 0

            #send afk message to server
            # pyautogui.write('t')
            # pyautogui.write("automated message: back")
            # pyautogui.press('enter')

        #state machine
        match state:
            case 0:
                
                #detect activation shortcut
                if keyboard.is_pressed('ctrl+i'):

                    #indicate state change in terminal
                    print("clicking")

                    #switch to clicking state
                    state = CLICKING

                    doTorchAction()

                    #send afk message to server
                    # pyautogui.write('t')
                    # pyautogui.write("automated message: afk")
                    # pyautogui.press('enter')

                    #reset timers
                    clickingTimer = time.time()
                    afkMessageTimer = time.time()

            case 1:

                #detect user movement in game
                if (keyboard.is_pressed('e') or 
                    keyboard.is_pressed('escape') or 
                    keyboard.is_pressed('space')):

                    #indicate state change in terminal
                    print("inactive")

                    #switch to inactive state
                    state = INACTIVE

                    #send afk message to server
                    # pyautogui.write('t')
                    # pyautogui.write("automated message: back")
                    # pyautogui.press('enter')

                #detect user entering typing menu
                elif keyboard.is_pressed('t'):

                    #indicate state change in terminal
                    print("typing")
                    
                    #switch to state 2
                    state = TYPING

                else:

                    #check if last click was more than 5 seconds ago
                    if (time.time() - clickingTimer) > 5:

                        doTorchAction()

                        #reset timer
                        clickingTimer = time.time()

                    #check if last message was sent more than 15 minutes ago
                    if (time.time() - afkMessageTimer) > 10*60:
                        
                        messageNumberTracker = sendAfkMessage(messageNumberTracker)

                        #reset timer
                        afkMessageTimer = time.time()

            case 2:

                #detect if typing menu is exited
                if (keyboard.is_pressed('enter') or 
                    keyboard.is_pressed('escape')):

                    #indicate state change in terminal
                    print("clicking")

                    #switch to clciking state
                    state = CLICKING

                    #add delay so enter and escape are not immediately detected in the clicking state
                    #600ms delay, some googling says key presses are 300ms on the long end, using safety factor of two
                    time.sleep(0.6)

    #calulate time to wait before next poll should occur
    timeToIdle = 50E-3 - (time.time() - pollFrequencyTimer)
    # print("Idle time", timeToIdle * 1000, " ms") #debug only

    #only sleep if delay is a valid duration
    if timeToIdle > 0:
        time.sleep(timeToIdle)

            
#exit program
print("Exit key pressed. Program done.\n")