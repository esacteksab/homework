from time import time
import SimpleHTTPServer
import SocketServer


def elapsed_time(_since=time()):
    return time() - _since


class SillyHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        if elapsed_time() < 45:
            self.send_error(503)
        else:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'<!DOCTYPE html><html><body><h2>Foo bar</h2></body></html>')

httpd = SocketServer.TCPServer(('localhost', 8000), SillyHandler)
print('Serving http://{addr[0]}:{addr[1]}/'.format(addr=httpd.socket.getsockname()))
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    print('\nKeyboard interrupt received, exiting.')
    httpd.socket.close()
