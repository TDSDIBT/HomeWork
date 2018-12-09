# -*- coding: utf-8 -*-
import socketserver


class MyServer(socketserver.BaseRequestHandler):

    def handle(self):
        conn = self.request
        print(conn)
        # conn.sendall('我是多线程')
        Flag = True
        while Flag:
            data = conn.recv(1024)
            text = '请重新输入.'
            conn.sendall(text.encode())


if __name__ == '__main__':
    server = socketserver.ThreadingTCPServer(('127.0.0.1', 8080), MyServer)
    server.serve_forever()
