import logging
logger = logging.getLogger(__name__)

import paramiko
import subprocess

class SSH(object):
    def __init__(self, hostname, username, password = None, pkey = None):
        self.arguments = {k: v for k, v in locals().items() if k is not 'self' if v is not None}
        self.credentials = {k: v for k, v in self.arguments.items() if k is not 'hostname'}
        self.__transport = None
        self._ftp = None
        self._ssh = None
        
        self.connect_server()
        
    def connect_server(self):
        transport = paramiko.Transport((self.arguments['hostname'], 22))
        transport.default_window_size=paramiko.common.MAX_WINDOW_SIZE
        transport.packetizer.REKEY_BYTES = pow(2, 40)
        transport.packetizer.REKEY_PACKETS = pow(2, 40)
        transport.connect(**self.credentials)
        self.__transport = transport
        
    def sftp(self):
        self._ftp = paramiko.SFTPClient.from_transport(self.__transport)
        
    def ssh(self, command):
        self._ssh = paramiko.SSHClient()
        self._ssh._transport = self.__transport
        stdin, stdout, stderr = self._ssh.exec_command(command)
        ret = stderr.read()
        if not ret:
            ret = stdout.read()
        return ret
    
    @staticmethod
    def exec_command(command):
        ret = subprocess.call(command, shell=True, stdout=subprocess.PIPE)
        return ret
        
    def close(self):
        self.__transport.close()
            