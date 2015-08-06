import os.path

from socketio.server import SocketIOServer
from pyramid.paster import get_app
from gevent import monkey; monkey.patch_all()

def main():
    app = get_app(os.path.join(os.path.dirname(__file__), 'development.ini'))
    print 'Listening on port http://0.0.0.0:8080 and on port 10843 (flash policy server)'

    SocketIOServer(('0.0.0.0', 8090), app,
        resource="socket.io", policy_server=True,
        policy_listener=('0.0.0.0', 10843)).serve_forever()

if __name__ == '__main__':
    main()
