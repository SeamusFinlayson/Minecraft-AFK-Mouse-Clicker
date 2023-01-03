#filename: keepMinecraftAlive.py
#author: Seamus Finlayson
#date: 2022-12-26

#include pip installed packages
import pyautogui
import keyboard
import pygetwindow

#include packages from the standard library
import time
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

#variable to track time since the player last ate
eatingTimer = time.time()

#place and break torch
def doTorchAction():
        
    #indictate action in terminal
    print("doing torch action")

    pyautogui.click(button='right') #place torch
    pyautogui.click() #break torch

#attack monster
def doAttackingAction():

    #indictate action in terminal
    print("doing attacking action")

    pyautogui.click() #swing weapon

#eat food to regenerate hunger bar
def doEatAction():

    #indictate action in terminal
    print("doing eating action")

    #start eating
    pyautogui.mouseDown(button='right')

    #wait for eating to finish
    time.sleep(2)

    #release button when finished
    pyautogui.mouseUp(button='right')

#variable for tracking which message to send
NUMBER_OF_MESSAGES = 3

#initialize send random initial message
messageNumberTracker = random.randint(0, NUMBER_OF_MESSAGES)

#send a random afk message
def sendAfkMessage(messageNumber):

    #tell user a message has been sent in terminal
    print("message sent to chat")

    #open chat
    pyautogui.write('t')

    #clear chat before sending message
    pyautogui.press('ctrl+a')
    pyautogui.press('backspace')

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
#state 0 => inactive state, do nothing
INACTIVE = 0
#state 1 => torch placing state, placing torches every 5 seconds
TORCH_PLACING = 1
#state 2 => typing state, ignore certain deactivating keys for state 1 while user is typing
TYPING = 2
#state 3 => attacking state, attacks mobs in a mob farm while the user is afk
ATTACKING = 3
#set initial state to inactive
state = INACTIVE
#remember which state the typing state was entered from to return to that state
stateLast = TORCH_PLACING
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

            #change state to inactive
            state = INACTIVE

        #state machine
        match state:
            case 0:
                
                #detect activation shortcut
                if keyboard.is_pressed('ctrl+i'):

                    #indicate state change in terminal
                    print("torch placing")

                    #switch to torchplacing state
                    state = TORCH_PLACING

                    doTorchAction()

                    #reset timers
                    clickingTimer = time.time()
                    afkMessageTimer = time.time()

                if keyboard.is_pressed('ctrl+k'):

                    #indicate state change in terminal
                    print("attacking")

                    #switch to torchplacing state
                    state = ATTACKING

                    doAttackingAction()

                    #reset timers
                    clickingTimer = time.time()
                    afkMessageTimer = time.time()

            case 1:

                #when the user presses the windows key
                if keyboard.is_pressed('win'):

                    #reset timers
                    afkMessageTimer = time.time()
                    clickingTimer = time.time()

                    #indicate reset in terminal
                    #print("message timer reset because win key was pressed") #debug only

                #detect user movement in game
                if (keyboard.is_pressed('e') or 
                    keyboard.is_pressed('escape') or 
                    keyboard.is_pressed('space')):

                    #indicate state change in terminal
                    print("inactive")

                    #switch to inactive state
                    state = INACTIVE

                #detect user entering typing menu
                elif keyboard.is_pressed('t'):

                    #indicate state change in terminal
                    print("typing")
                    
                    #switch to state 2
                    state = TYPING

                    #tell state 2 to come back to this state
                    stateLast = TORCH_PLACING

                #detect user request to switch to attacking state
                elif keyboard.is_pressed('ctrl+k'):

                    #indicate state change in terminal
                    print("attacking")

                    #change state
                    state = ATTACKING

                    doAttackingAction()

                else:

                    #check if last click was more than 5 seconds ago
                    if (time.time() - clickingTimer) > 5:

                        doTorchAction()

                        #reset timer
                        clickingTimer = time.time()

                    #check if last message was sent more than 15 minutes ago
                    if (time.time() - afkMessageTimer) > 20*60:
                        
                        messageNumberTracker = sendAfkMessage(messageNumberTracker)

                        #reset timer
                        afkMessageTimer = time.time()

            case 2:

                #detect if typing menu is exited
                if (keyboard.is_pressed('enter') or 
                    keyboard.is_pressed('escape')):

                    #indicate state change in terminal
                    if stateLast == TORCH_PLACING:
                        print("torch placing")
                    elif stateLast == ATTACKING:
                        print("attacking")

                    #switch to torch placing state
                    state = stateLast

                    #add delay so enter and escape are not immediately detected in the clicking state
                    #600ms delay, some googling says key presses are 300ms on the long end, using safety factor of two
                    time.sleep(0.6)

            case 3:

                #when the user presses the windows key
                if keyboard.is_pressed('win'):

                    #reset timers
                    afkMessageTimer = time.time()
                    clickingTimer = time.time()

                    #indicate reset in terminal
                    #print("message timer reset because win key was pressed") #debug only

                #detect user movement in game
                if (keyboard.is_pressed('e') or 
                    keyboard.is_pressed('escape') or 
                    keyboard.is_pressed('space')):

                    #indicate state change in terminal
                    print("inactive")

                    #switch to inactive state
                    state = INACTIVE

                #detect user entering typing menu
                elif keyboard.is_pressed('t'):

                    #indicate state change in terminal
                    print("typing")
                    
                    #switch to state 2
                    state = TYPING

                    #tell state 2 to come back to this state
                    stateLast = ATTACKING

                #detect user request to switch to torch placing state
                elif keyboard.is_pressed('ctrl+i'):

                    #indicate state change in terminal
                    print("torch placing")

                    #change state
                    state = TORCH_PLACING

                    doTorchAction()

                else:

                    #check if last click was more than 5 seconds ago
                    if (time.time() - clickingTimer) > 5:

                        doAttackingAction()

                        #reset timer
                        clickingTimer = time.time()

                    #check if last message was sent more than 15 minutes ago
                    if (time.time() - afkMessageTimer) > 20*60:
                        
                        messageNumberTracker = sendAfkMessage(messageNumberTracker)

                        #reset timer
                        afkMessageTimer = time.time()

                    #check if last meal was more than 15 minutes ago
                    if (time.time() - eatingTimer) > 15*60:

                        doEatAction()

                        #reset timer
                        eatingTimer = time.time()

    #calulate time to wait before next poll should occur
    timeToIdle = 50E-3 - (time.time() - pollFrequencyTimer)
    # print("Idle time", timeToIdle * 1000, " ms") #debug only

    #only sleep if delay is a valid duration
    if timeToIdle > 0:
        time.sleep(timeToIdle)

#exit program
print("Exit key pressed. Program done.\n")