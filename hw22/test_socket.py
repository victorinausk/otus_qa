import socket
import sys
from html.entities import name2codepoint
from html.parser import HTMLParser

from py_w3c.validators.html.validator import HTMLValidator
from six import unichr


class Http:
    """Http thought socket class"""

    class MyHTMLParser(HTMLParser):
        def handle_starttag(self, tag, attrs):
            print("Start tag:", tag)
            for attr in attrs:
                print("     attr:", attr)

        def handle_endtag(self, tag):
            print("End tag  :", tag)

        def handle_data(self, data):
            print("Data     :", data)

        def handle_comment(self, data):
            print("Comment  :", data)

        def handle_entityref(self, name):
            c = unichr(name2codepoint[name])
            print("Named ent:", c)

        def handle_charref(self, name):
            if name.startswith('x'):
                c = unichr(int(name[1:], 16))
            else:
                c = unichr(int(name))
            print("Num ent  :", c)

        def handle_decl(self, data):
            print("Decl     :", data)

    def __init__(self, url, method, header, port):
        self.url = url
        self.method = method
        self.header = header
        self.port = int(port)
        self.connection = None
        self.reply = None
        self.parser = self.MyHTMLParser()

    def create_socket(self):
        """create socket"""
        try:
            self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            return self.connection
        except socket.error:
            print('Failed to create socket')
            sys.exit()

    def connect_server(self):
        """Connect to remote server"""
        print('# Connecting to server, ' + self.url)
        self.connection.connect((self.url, self.port))

    def send_data(self):
        """Send data to remote server"""
        print('# Sending data to server')
        request = b''
        request += str.encode(self.method)
        request += b' / '
        request += str.encode(self.header) + b'\r\n'
        request += b'\r\n'
        try:
            self.connection.sendall(request)
        except socket.error:
            print("Send failed")
            sys.exit()

    def receive_data(self):
        """Receive data"""
        print('# Receive data from server')
        self.reply = self.connection.recv(4096)
        while True:
            self.reply += self.connection.recv(4096)
            if "</html>" in str(self.reply):
                break
        return self.reply

    def get_parsedcodes(self):
        """Get Header and parsed codes"""
        data = self.reply.split(b'\r\n')
        data.pop()
        data = data[0]
        header = data.decode()
        result = header.splitlines()
        retcode = result[0].split(' ')[1]
        retresult = result[0].split(' ')[2]
        print("-------------")
        print('Header:', header)
        print("Return code:", retcode)
        print("Return result:", retresult)
        return retcode, retresult

    def get_parsedbody(self):
        """
        parse html by MyHTMLParser
        :return:
        """
        self.parser.feed(self.reply.decode())

    def is_socket_response_html(self):
        """
        Validate socket response  for  html syntax
        :return:
        """
        val = HTMLValidator()
        return val.validate_fragment(self.reply.decode())

    def __del__(self):
        self.connection = None


def test_socket(request):
    url = request.config.getoption('--opencart_url')
    method = request.config.getoption('--method')
    header = request.config.getoption('--header')
    port = request.config.getoption('--port')

    r = Http(url, method, header, port)
    r.create_socket()
    r.connect_server()
    r.send_data()
    r.receive_data()
    retcode, retresult = r.get_parsedcodes()

    assert retcode == '200' and retresult == 'OK'

    r.get_parsedbody()

    assert r.is_socket_response_html()
