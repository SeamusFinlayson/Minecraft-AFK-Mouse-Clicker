# Minecraft-AFK-Mouse-Clicker

This Python script is designed to keep a Minecraft character active while a player is away from their keyboard (AFK) using automated mouse clicks. Minecraft realms and servers will automatically disconnect players who have been idle for too long. Minecraft players, however, often create farms that will collect resources for them without any input from the player and being disconnected will interrupt this automatic resource collection. This script allows the player to be AFK for hours at a time and not disconnect from the game.

This script will automatcailly either repeatedly place and break a torch in the game OR attack mobs in a kill chamber and eat in the game.

Key presses will only be registered while Minecraft in multiplayer is the active window.

## Setup

You will need to download this script and install [PyAutoGUI](https://pypi.org/project/PyAutoGUI/), [keyboard](https://pypi.org/project/keyboard/), and [PyGetWindow](https://pypi.org/project/PyGetWindow/) using pip.

### VS Code

If you wish to modify this script I recommend doing that in [VS Code](https://code.visualstudio.com/) because it is light weight and easy for your computer to run in the background. You can find tutorials to set this up on YouTube.

### Windows 11 Command Line

**If you just want to run the script** follow [this tutorial](https://www.dataquest.io/blog/installing-python-on-windows/) to install python and [this tutorial](https://www.dataquest.io/blog/install-pip-windows/) to install the pip package manager. You only need python 3, not Python 2 or Anaconda. Then run the three commands below in the Windows PowerShell.

`pip install pyautogui`

`pip install keyboard` 

`pip install pygetwindow`

Then copy the path of the keepMionecraftAlive.py file you downloaded file by right clicking on it and selecting *Copy as path* then go back to the Windows PowerShell and enter `python <the path you copied>` without the angle brackets. Then the script should run in the terminal.

## How to Use the Script

### Torch Placing Mode

Use this mode if you are using a purely passive farm and just need to remain connected to the server or realm.

1. Run the script
2. In Minecraft face a wall and equip a torch
3. Press ctrl+i to enter torch placing mode
4. Go AFK then come back
5. Press ctrl+u, jump (press the space key), go to the game menu (press escape), or enter your inventory (press e) to exit torch placing mode
6. Repeat steps 2-5 as many times as you want or go to attack mode instead
7. When you're done press ctrl+o to terminate the script

### Attacking Mode

Use this mode if you are using an Ender Ender or Mob Grinder and want to kill mobs while AFK. This mode will also automatically eat food to keep your character alive.

1. Run the script
2. In Minecraft equip a sword to your right hand and food to your left hand, then face the kill chamber.
3. Press ctrl+k to enter attacking mode
4. Go AFK then come back
5. Press ctrl+u, jump (press the space key), go to the game menu (press escape), or enter your inventory (press e) to exit attacking mode
6. Repeat steps 2-5 as many times as you want or go to torch placing mode instead
7. When you're done press ctrl+o to terminate the script

## Don't Have a Farm?

Follow one of these tutorials:
- [Build an Iron Farm](https://www.youtube.com/watch?v=xDJtXznj8Fg)
- [Build a Mob Grinder](https://www.youtube.com/watch?v=USL0h4-nul4)
- [Build an Ender Ender](https://www.youtube.com/watch?v=nh8voJScSbw)

