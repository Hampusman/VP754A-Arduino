import socket
import threading
import time
from arduino import Arduino


class TcpServer:
    def __init__(self, host: str = '', port: int = 1337, max_users: int = 5):
        self._host = host
        self._port = port
        self._max_users = max_users
        self._arduino = Arduino()
        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._subscribers = []
        self._server_stop = threading.Event()
        self._subscriber_thread = threading.Thread(target=self._subscription, daemon=True)
        self._subscriber_thread.start()

    def run(self) -> None:
        try:
            self._server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self._server.bind((self._host, self._port))
            self._server.listen(5)
            print(f'Server started.\nActive connections {threading.active_count() - 3}/{self._max_users}\n')
            while not self._server_stop.is_set():
                connection, address = self._server.accept()
                thread = threading.Thread(target=self._handle_client, args=(connection, address), daemon=True)
                thread.start()
                print(f'Active connections {threading.active_count() - 3}/{self._max_users}\n')
        except KeyboardInterrupt:
            print('Server interrupted...')
        finally:
            self._stop_threads()
            self._server.close()

    def _handle_client(self, client: socket.socket, address: str):
        print(f'{address} connected.')
        try:
            while not self._server_stop.is_set():
                data = client.recv(1024)
                if not data:
                    break
                data = data.decode('UTF-8')
                data = data.lower()
                data = data.strip()
                print(f'Data received: {data}, from {address}')
                match data:
                    case 'get':
                        value = self._arduino.value
                        print(f'Sent value: {value}')
                        client.sendall(f'{str(value)}\n'.encode('UTF-8'))
                    case 'subscribe':
                        self._subscribers.append(client)
                        print(f'Subscription started for {address}')
                    case 'unsubscribe':
                        self._subscribers.remove(client)
                    case 'echo':
                        client.sendall(f'Echo: {address}, {data}\n'.encode('UTF-8'))
                    case _:
                        client.sendall(f'Unknown command: {data}\n'.encode('UTF-8'))
        except ConnectionResetError:
            print(f'Client {address} disconnected.')
        finally:
            if client in self._subscribers:
                self._subscribers.remove(client)
            client.close()
            print(f'Connection with {address} closed.')
            print(f'Active connections {threading.active_count() - 3}/{self._max_users}\n')

    def _subscription(self) -> None:
        while not self._server_stop.is_set():
            if self._subscribers:
                for client in self._subscribers:
                    client.sendall(f'{str(self._arduino.value)}\n'.encode('UTF-8'))
                    time.sleep(0.1)

    def _stop_threads(self):
        self._arduino.stop()
        time.sleep(1)
        self._server_stop.set()
