import socket

def ping_livesplit_server():
    x = 0
    while x < 6:
        try:
            # Create socket and connect to LiveSplit Server
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(("localhost", 16834))
            return True
        except ConnectionRefusedError:
            x += 1
    return False


def send_command(command: str):
    try:
        # Create socket and connect to LiveSplit Server
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(("localhost", 16834))
            s.sendall(f"{command}\r\n".encode('utf-8'))
            data: str = s.recv(1024).decode('UTF-8')
        return data
    except ConnectionError:
        return None