'''
作者：facert
链接：https://zhuanlan.zhihu.com/p/28798090
来源：知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
'''

def handle(self):
        try:
            sock = self.connection
            addrtype = ord(self.decrypt(sock.recv(1)))      # receive addr type
            if addrtype == 1:
                addr = socket.inet_ntoa(self.decrypt(self.rfile.read(4)))   # get dst addr
            elif addrtype == 3:
                addr = self.decrypt(
                    self.rfile.read(ord(self.decrypt(sock.recv(1)))))       # read 1 byte of len, then get 'len' bytes name
            else:
                # not support
                logging.warn('addr_type not support')
                return
            port = struct.unpack('>H', self.decrypt(self.rfile.read(2)))    # get dst port into small endian
            try:
                logging.info('connecting %s:%d' % (addr, port[0]))
                remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                remote.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                remote.connect((addr, port[0]))         # connect to dst
            except socket.error, e:
                # Connection refused
                logging.warn(e)
                return
            self.handle_tcp(sock, remote)
        except socket.error, e:
            logging.warn(e)