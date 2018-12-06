'''
作者：facert
链接：https://zhuanlan.zhihu.com/p/28798090
来源：知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
'''

class Socks5Server(SocketServer.StreamRequestHandler):
    ''' RequesHandlerClass Definition '''
    def handle_tcp(self, sock, remote):
        try:
            fdset = [sock, remote]
            while True:
                r, w, e = select.select(fdset, [], [])      # use select I/O multiplexing model
                if sock in r:                               # if local socket is ready for reading
                    data = sock.recv(4096)
                    if len(data) <= 0:                      # received all data
                        break
                    result = send_all(remote, self.encrypt(data))   # send data after encrypting
                    if result < len(data):
                        raise Exception('failed to send all data')

                if remote in r:                             # remote socket(proxy) ready for reading
                    data = remote.recv(4096)
                    if len(data) <= 0:
                        break
                    result = send_all(sock, self.decrypt(data))     # send to local socket(application)
                    if result < len(data):
                        raise Exception('failed to send all data')
        finally:
            sock.close()
            remote.close()

    def encrypt(self, data):
        return data.translate(encrypt_table)

    def decrypt(self, data):
        return data.translate(decrypt_table)

    def send_encrypt(self, sock, data):
        sock.send(self.encrypt(data))

    def handle(self):
        try:
            sock = self.connection        # local socket [127.1:port]
            sock.recv(262)                # Sock5 Verification packet
            sock.send("\x05\x00")         # Sock5 Response: '0x05' Version 5; '0x00' NO AUTHENTICATION REQUIRED
            # After Authentication negotiation
            data = self.rfile.read(4)     # Forward request format: VER CMD RSV ATYP (4 bytes)
            mode = ord(data[1])           # CMD == 0x01 (connect)
            if mode != 1:
                logging.warn('mode != 1')
                return
            addrtype = ord(data[3])       # indicate destination address type
            addr_to_send = data[3]
            if addrtype == 1:             # IPv4
                addr_ip = self.rfile.read(4)            # 4 bytes IPv4 address (big endian)
                addr = socket.inet_ntoa(addr_ip)
                addr_to_send += addr_ip
            elif addrtype == 3:           # FQDN (Fully Qualified Domain Name)
                addr_len = self.rfile.read(1)           # Domain name's Length
                addr = self.rfile.read(ord(addr_len))   # Followed by domain name(e.g. www.google.com)
                addr_to_send += addr_len + addr
            else:
                logging.warn('addr_type not support')
                # not support
                return
            addr_port = self.rfile.read(2)
            addr_to_send += addr_port                   # addr_to_send = ATYP + [Length] + dst addr/domain name + port
            port = struct.unpack('>H', addr_port)       # prase the big endian port number. Note: The result is a tuple even if it contains exactly one item.
            try:
                reply = "\x05\x00\x00\x01"              # VER REP RSV ATYP
                reply += socket.inet_aton('0.0.0.0') + struct.pack(">H", 2222)  # listening on 2222 on all addresses of the machine, including the loopback(127.0.0.1)
                self.wfile.write(reply)                 # response packet
                # reply immediately
                if '-6' in sys.argv[1:]:                # IPv6 support
                    remote = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
                else:
                    remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                remote.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)       # turn off Nagling
                remote.connect((SERVER, REMOTE_PORT))
                self.send_encrypt(remote, addr_to_send)      # encrypted
                logging.info('connecting %s:%d' % (addr, port[0]))
            except socket.error, e:
                logging.warn(e)
                return
            self.handle_tcp(sock, remote)
        except socket.error, e:
            logging.warn(e)