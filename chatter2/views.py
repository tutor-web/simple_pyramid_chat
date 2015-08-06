from socketio.namespace import BaseNamespace
from socketio import socketio_manage
from socketio.mixins import RoomsMixin, BroadcastMixin


def index(request):
    """ Base view to load our template """
    return {}


class ChatNamespace(BaseNamespace, RoomsMixin, BroadcastMixin):
    def on_chat(self, msg):
        self.broadcast_event('chat', msg)

    def recv_connect(self):
        self.broadcast_event('user_connect')

    def recv_disconnect(self):
        for namespaceRoom in self.session['rooms'].copy():
            self.on_leave(namespaceRoom.replace(self.ns_name + '_', '', 1))
        self.disconnect(silent=True)

    def on_join(self, room):
        self.emit_to_room(room, 'room_join',
            self.socket.session['nickname'])
        self.join(room)

    def on_leave(self, room):
        self.emit_to_room(room, 'room_leave',
            self.socket.session['nickname'])
        self.leave(room)



from pyramid.response import Response
def socketio_service(request):
    socketio_manage(request.environ,
                    {'/chat': ChatNamespace},
                    request=request)

    return Response('')

