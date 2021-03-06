import random

from socketio.namespace import BaseNamespace
from socketio import socketio_manage
from socketio.mixins import RoomsMixin, BroadcastMixin


def index(request):
    """ Base view to load our template """
    return {}


class ChatNamespace(BaseNamespace, RoomsMixin, BroadcastMixin):
    def recv_connect(self):
        self.socket.session['nickname'] = "user-%s" % random.randrange(1000, 9999)

    def on_nick(self, nick):
        self.socket.session['nickname'] = nick
        self.socket.send_packet(dict(
            type="event",
            name="set_nick",
            args=[self.socket.session['nickname']],
            endpoint=self.ns_name,
        ))

    def recv_disconnect(self):
        for namespaceRoom in self.session['rooms'].copy():
            self.on_leave(namespaceRoom.replace(self.ns_name + '_', '', 1))
        self.disconnect(silent=True)

    def on_session_start(self, room, remainingSeconds, maxSeconds):
        self.emit_to_room(room, 'session_start',
            remainingSeconds, maxSeconds)

    def on_session_stop(self, room):
        self.emit_to_room(room, 'session_stop',
            self.socket.session['nickname'])

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

