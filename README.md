# OW-TAS-savefile-converter
v0.2.0
This version is incompatible with saves before v0.2.0

Converts global variables copied from Overwatch Workshop Inspector to a savefile that can be pasted into the game

run the converter, provide it with the pasted text, take the produced produced output and paste it at the bottom of the mode

## Inspector Log format specifications:

The inspector log file is formatted a series of commands. Following all the commands will reconstruct the data to the point of the last log. Logs are sent every time data is changed in the mode so the log file is a form of autosave.

Commands are an identifying character followed by params.

Log Commands: 
- m - set map
- n - make a new bot
- b - change to bot
- x - remove bot
- r - reset bot data
- c - cut bot's data
- a - append to bot's var
- p - set bot init pos
- f - set bot init facing
- t - set bot total framecount

Bot append uses a param that is a keyword:
- thr - throttle value
- thrT - throttle timing
- fac - facing value
- facT - facing timing
- wep - weapon
- wepT - weapon timing
- butT - button; takes additional param i at end, the index of the button in allButtons, ordered same as drop-down for buttons in the overwatch workshop. can view it in mode.ow


bot data output format:
hero, team, thr, thrT, fac, facT, initBut, butT, wep, wepT, fac x, y, z, pos x, y, z, framecount