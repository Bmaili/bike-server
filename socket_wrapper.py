class SocketWrapper(object):
    """包装客户端套接字类"""

    def __init__(self, sock):
        self.sock = sock

    def recv_data(self):
        """接收数据"""

        return self.sock.recv(512).decode("utf-8").strip()

    def send_data(self, messages):
        """发送数据"""

        messages += "\r\n"
        return self.sock.send(messages.encode("utf-8"))

    def close(self):
        '''下线'''

        return self.sock.close()
