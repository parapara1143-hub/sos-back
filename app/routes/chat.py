from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..extensions import db
from ..models.message import Message
from ..sockets.events import emit_chat_message

bp = Blueprint("chat", __name__)

@bp.get("/room/<int:room_id>/history")
@jwt_required()
def history(room_id):
    msgs = Message.query.filter_by(room_id=room_id).order_by(Message.id.asc()).all()
    return {"items": [{"id": m.id, "user_id": m.user_id, "content": m.content} for m in msgs]}

@bp.post("/room/<int:room_id>/message")
@jwt_required()
def post_message(room_id):
    uid = int(get_jwt_identity())
    d = request.get_json() or {}
    msg = Message(room_id=room_id, user_id=uid, content=d.get("content","").strip())
    db.session.add(msg); db.session.commit()
    emit_chat_message(room_id, msg)
    return {"id": msg.id}
