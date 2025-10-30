
from flask import Blueprint, request, send_from_directory, current_app
from flask_jwt_extended import jwt_required
from ..services.storage import save_local, presign_s3
import os, uuid

bp = Blueprint("files", __name__)

@bp.post("/upload")
@jwt_required()
def upload():
    if current_app.config.get("STORAGE_PROVIDER","local") == "s3":
        return {"error":"use /api/files/presign for S3 uploads"}, 400
    if "file" not in request.files:
        return {"error":"file required"}, 400
    url = save_local(request.files["file"])
    return {"url": url}, 201

@bp.post("/presign")
@jwt_required()
def presign():
    if current_app.config.get("STORAGE_PROVIDER","local") == "local":
        return {"error":"local storage doesn't require presign"}, 400
    data = request.get_json() or {}
    key = data.get("key") or f"uploads/{uuid.uuid4().hex}"
    content_type = data.get("content_type","application/octet-stream")
    put_url, public_url = presign_s3(key, content_type)
    return {"put_url": put_url, "public_url": public_url}

@bp.get("/serve/<path:filename>")
def serve(filename):
    base = current_app.config.get("STORAGE_LOCAL_DIR","uploads")
    return send_from_directory(base, filename)
