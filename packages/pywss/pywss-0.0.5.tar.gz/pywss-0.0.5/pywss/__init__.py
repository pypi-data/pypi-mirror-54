import socketserver
import json

from socket import socket, getdefaulttimeout
from _socket import AF_INET, SOCK_STREAM

from pywss.protocol import WebSocketProtocol
from pywss.middlewares import *
from pywss.public import *
from pywss.route import *

logging.basicConfig(format="%(asctime)s %(funcName)s[lines-%(lineno)d]: %(message)s")
logger = logging.getLogger(__name__)


class WsSocket(socket):
    __slots__ = ["_io_refs", "_closed", "__route__"]

    def __init__(self, family=-1, type=-1, proto=-1, fileno=None):
        if fileno is None:
            if family == -1:
                family = AF_INET
            if type == -1:
                type = SOCK_STREAM
            if proto == -1:
                proto = 0
        super(WsSocket, self).__init__(family, type, proto, fileno)

    def accept(self):
        fd, addr = self._accept()
        sock = WsSocket(self.family, self.type, self.proto, fileno=fd)
        if getdefaulttimeout() is None and self.gettimeout():
            sock.setblocking(True)
        return sock, addr

    def ws_recv(self, bufsize: int, flags: int = ...):
        return WebSocketProtocol.decode_msg(self.recv(bufsize))

    def ws_send(self, data, flags: int = ...):
        self.send(WebSocketProtocol.encode_msg(json.dumps(data, ensure_ascii=False).encode('utf-8')))


class MyServerTCPServer(socketserver.TCPServer):

    def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True):
        socketserver.BaseServer.__init__(self, server_address, RequestHandlerClass)
        self.socket = WsSocket(self.address_family, self.socket_type)
        if bind_and_activate:
            try:
                self.server_bind()
                self.server_activate()
            except:
                self.server_close()
                raise

    def serve_forever(self, poll_interval=0.5):
        if mwManager.radio_middleware:
            mwManager.radio_process()
        super(MyServerTCPServer, self).serve_forever(poll_interval)

    def verify_request(self, request, client_address):
        try:
            path, key = WebSocketProtocol.parsing(request.recv(1024))
            if path in Route.routes:
                request.send(key)
                request.__route__ = path
                return True
        except:
            pass
        return False


class MyServerThreadingMixIn(socketserver.ThreadingMixIn):
    """开启新线程处理socket"""


class SocketHandler:

    def __init__(self, request, client_address, server):
        self.request = request
        self.client_address = client_address
        self.func = Route.get(self.request.__route__)
        try:
            self.setup()
            self.handle()
        except:
            pass
        finally:
            self.finish()

    def setup(self):
        self.conn = mwManager.daemon_process(self, self.request)
        if not self.conn:
            self.conn = Connector(self.request, self.client_address)
        ConnectManager.add_connector(self.conn.name, self.conn.client_address, self.conn)
        logger.info('New Connect {} From {}'.format(self.conn.name, self.conn.client_address))
        if not radio_queue.qsize():
            radio_queue.put(RADIO_START)

    def handle(self):
        error_count = 0
        try:
            while error_count < PublicConfig.ERROR_COUNT_MAX:
                info = mwManager.process(self.request, self.request.ws_recv(1024), self.func)
                if info is ERROR_FLAG:
                    error_count += 1
                elif info:
                    self.request.ws_send(info)
                else:
                    error_count += 4
        except:
            pass

    def finish(self):
        logger.warning('%s:%s Connect Close' % self.client_address)
        try:
            ConnectManager.clear(self.conn.name, self.conn.client_address, self.conn.clear_level)
        except:
            pass


class Pyws(MyServerThreadingMixIn, MyServerTCPServer):

    def __init__(self,
                 routes_module,
                 address='0.0.0.0', port=8866,
                 RequestHandlerClass=SocketHandler,
                 request_queue_size=5,
                 middleware=None,
                 logging_level=logging.INFO):
        logger.setLevel(logging_level)
        logger.info('Server Start ...')
        logger.info('Server Address is %s:%d' % (address, port))
        server_address = (address, port)
        self.add_routes(routes_module)
        self.add_middleware(middleware)
        self.request_queue_size = request_queue_size
        super(Pyws, self).__init__(server_address, RequestHandlerClass)

    def add_routes(self, module):
        Route.add_routes(module)

    def add_middleware(self, middleware):
        mwManager.auto_add(middleware)
