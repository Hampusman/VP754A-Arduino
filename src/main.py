from tcp_server import TcpServer
from arduino import Arduino

def test():
    arduino = Arduino()
    arduino.debug()

def main():
    server = TcpServer()
    server.run()


if __name__ == '__main__':
    main()