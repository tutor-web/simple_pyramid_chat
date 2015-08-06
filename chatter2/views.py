from socketio.namespace import BaseNamespace
from socketio import socketio_manage
from socketio.mixins import RoomsMixin, BroadcastMixin


def index(request):
    """ Base view to load our template """
    return {}


class ChatNamespace(BaseNamespace, RoomsMixin, BroadcastMixin):
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

    def on_room_message(self, room, msg):
        self.emit_to_room(room, 'room_message',
            self.socket.session['nickname'], msg)


from pyramid.response import Response
def socketio_service(request):
    socketio_manage(request.environ,
                    {'/chat': ChatNamespace},
                    request=request)

    return Response('')

