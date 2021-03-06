import logging
from gevent.pywsgi import WSGIServer
from .handler import WebSocketHandler

logger = logging.getLogger(__name__)

class WebSocketServer(WSGIServer):
    handler_class = WebSocketHandler
    debug_log_format = (
        '-' * 80 + '\n' +
        '%(levelname)s in %(module)s [%(pathname)s:%(lineno)d]:\n' +
        '%(message)s\n' +
        '-' * 80
    )

    def __init__(self, *args, **kwargs):
        self.debug = kwargs.pop('debug', False)
        self.pre_start_hook = kwargs.pop('pre_start_hook', None)
        self.clients = {}

        super(WebSocketServer, self).__init__(*args, **kwargs)

    def handle(self, socket, address):
        handler = self.handler_class(socket, address, self)
        handler.handle()
