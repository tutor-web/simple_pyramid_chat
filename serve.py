import os.path

from socketio.server import SocketIOServer
from pyramid.paster import get_app
from gevent import monkey; monkey.patch_all()

INTERFACE = '0.0.0.0'
PORT_HTTP = 8090
PORT_POLICY = 10843

def main():
    app = get_app(os.path.join(os.path.dirname(__file__), 'development.ini'))
    print 'Listening on port http://%s:%d and on port %d (flash policy server)' % (
        INTERFACE,
        PORT_HTTP,
        PORT_POLICY,
    )

    SocketIOServer((INTERFACE, PORT_HTTP), app,
        resource="socket.io", policy_server=True,
        policy_listener=(INTERFACE, PORT_POLICY)).serve_forever()

if __name__ == '__main__':
    main()
