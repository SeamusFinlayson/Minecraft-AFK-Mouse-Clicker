#filename: keepMinecraftAlive.py
#author: Seamus Finlayson
#date: 2022-12-26

#include libraries
import pyautogui
import time
import keyboard
import pygetwindow

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
print("Press 'i' to turn clicking on.")
print("Press 'u' to turn clicking off. Clicking will automatically turn off when you jump, enter your inventory, or enter the game menu.")
print("Press 'o' (the letter) to terminate this program.")
print("Key presses are only registered when Minecraft is the active window and you are playing Multiplayer.")
print("*************************************************************")
print("stopped")

#initialize timer and polling frequency
startTime = time.time()

#variable to lock maximum polling frequency at 20Hz
startPoll = time.time()

#state machine setup and state meanings
#state = 0 => inactive state where nothing happens
#state = 1 => clicking on, placing torches every 5 seconds
state = 0

#flag to exit program
quit = False

#main loop
while not quit:

    #check time at which polling cycle starts
    startPoll = time.time()

    #check if minecraft in multiplayer is the active window
    windowTitle = str(pygetwindow.getActiveWindowTitle())
    if windowTitle.startswith("Minecraft ") and windowTitle.count("Multiplayer"):

        #detect exit key pressed
        if keyboard.is_pressed('o'):
            quit = True

        #turn clicking on on
        if keyboard.is_pressed('i'):
            if state == 0:
                print("started")
                state = 1

        #turn  clicking off
        if (keyboard.is_pressed('u') or 
            keyboard.is_pressed('e') or 
            keyboard.is_pressed('escape') or 
            keyboard.is_pressed('space')):
            if state == 1:
                print("stopped")
                state = 0

        #state machine
        match state:
            case 0:
                pass

            case 1:
                #check if start time is more than 5 seconds ago
                if (time.time() - startTime) > 5:

                    #place and break torch
                    print("placed")
                    pyautogui.click(button='right') #place torch
                    pyautogui.click() #break torch

                    #reset timer
                    startTime = time.time()

    #calulate time to wait before next poll should occur
    timeToIdle = 50E-3 - (time.time() - startPoll)
    # print("Idle time", timeToIdle * 1000, " ms") #debug only

    #only sleep if delay is a valid duration
    if timeToIdle > 0:
        time.sleep(timeToIdle)

            
#exit program
print("Exit key pressed. Program done.\n")