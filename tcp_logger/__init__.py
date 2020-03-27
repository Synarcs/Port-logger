import logging
import socket
import sys
import threading
import nmap

config_server_port = '127.0.0.1'


config_port = nmap.PortScanner()

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

    def Nwt(self,sourceIp,scanPort):
        nm =  nmap.PortScanner
        nm.scan(config_server_port,scanPort)
        if nm[config_server_port].has_tcp():
            logging.info(nm[config_server_port]['tcp'][scanPort])
        else:
            logging.info(nm[config_server_port].all_protocols())

    def ClientHandle(self, client_socket, ip, remote_port):
        data = client_socket.recv(64)
        self.Nwt(socket.gethostname(),remote_port)
        self.logger.info('connection from {0} {1}'.format(
            client_socket.getsockname(), data))
        client_socket.send('access denied 403'.encode('utf-8'))
        # client_socket.client_socket()

    def startListen(self, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        port_address = (config_server_port, int(port))
        # bind to the server port
        sock.bind(port_address)
        sock.listen(1)
        # self.ConfigureSocket()
        while True:
            client, address = sock.accept()
            print(address)
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
