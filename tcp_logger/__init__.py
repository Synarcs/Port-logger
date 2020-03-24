import logging
import socket
import sys
import threading


def ConfigLogger():
    logger = logging.getLogger(__name__)
    logging.basicConfig(
        filename='config_data.log',
        level=logging.DEBUG,
        format='[%(asctime)s] - %(message)s',
        datefmt='%Y:%D %H:%M:%S'
    )
    return logger


class HoneyPot():
    def __init__(self, ports, config_file):
        self.config_file = config_file
        self.ports = ports
        self.listener = {}
        if len(ports) > 1:
            self.logger = ConfigLogger()
            self.logger.info(self.ports)
            self.logger.info(self.config_file)
        else:
            ConfigLogger().logger.error("the file config is less")
            sys.exit(1)
        pass

    def ClientHandle(self, client_socket, ip, remote_port):

        data = client_socket.recv(64)
        self.logger.info('connection from {0} {1}'.format(
            client_socket.getsockname(), data))
        client_socket.send('access denied 403')
        client_socket.client_socket()

    def startListen(self, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        port_address = ('127.0.0.1', 1999)
        # bind to the server port
        sock.bind(port_address)
        sock.listen(1)
        # self.ConfigureSocket()
        while True:
            client, address = sock.accept()
            clientHandle = threading.Thread(
                target=self.ClientHandle, args=(client, address[0], address[1]))
            clientHandle.start()

    def Working(self):
        # each port is a client
        # incoming request start a new thread
        for _ports in self.ports:
            self.listener[_ports] = threading.Thread(
                target=self.startListen, args=(_ports,))
            self.listener[_ports].start()

    def run(self):
        self.Working()
