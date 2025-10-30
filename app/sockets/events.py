from flask_socketio import Namespace, emit, join_room
from ..extensions import socketio

def register_socket_events(sio):
    sio.on_namespace(RTNamespace('/rt'))

class RTNamespace(Namespace):
    def on_connect(self):
        emit('connected', {'ok': True})
    def on_join(self, data):
        room = str(data.get("room"))
        join_room(room)
        emit('joined', {'room': room})

def broadcast_incident(event, inc):
    socketio.emit(event, {
        "id": inc.id, "title": inc.title, "status": inc.status.value,
        "lat": inc.lat, "lon": inc.lon, "assignee_id": inc.assignee_id
    }, namespace="/rt")

def emit_chat_message(room_id, msg):
    socketio.emit("chat.message", {
        "room_id": room_id, "id": msg.id, "user_id": msg.user_id, "content": msg.content
    }, room=str(room_id), namespace="/rt")

def emit_integration_event(event, payload):
    socketio.emit(event, payload, namespace="/rt")
