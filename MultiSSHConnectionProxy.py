import paramiko
class MultiSSHConnectionProxy:
    '''
    This class is used to make a tunnel connection using paramiko. Use the first connection to instatiate the object.
    The second connection is done by using the method connect.
    This works like a proxy object becausa it's interface works just like a normal Paramiko's SSHConnection.
    '''
    def __init__(self,hostname, username, password, port=22, **kwargs):
        self.hostname, self.username, self.password, self.port = hostname, username, password, port
        self.first_connection = paramiko.SSHClient()
        self.first_connection.load_system_host_keys()
        self.first_connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.first_connection.connect(hostname= hostname, username= username, password= password,port= port, **kwargs)
        
    def connect(self, hostname, username, password, port=22, **kwargs):
        transport = self.first_connection.get_transport()
        local_addr = (self.hostname, self.port)
        dest_addr = (hostname, port)
        channel = transport.open_channel("direct-tcpip", dest_addr, local_addr)
        
        self.second_connection = paramiko.SSHClient()
        self.second_connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.second_connection.connect(hostname = hostname,username= username,password= password,port= port, sock = channel, **kwargs)
        
    def exec_command(self, *args, **kwargs):
        return self.second_connection.exec_command(*args, **kwargs)        
    
    def open_sftp(self):
        return self.second_connection.open_sftp()
        
        
    def __del__(self):
        self.first_connection.close()
        self.second_connection.close()