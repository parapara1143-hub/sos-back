
import os, uuid, boto3
from flask import current_app
from werkzeug.utils import secure_filename

def save_local(file_storage):
    base = current_app.config.get("STORAGE_LOCAL_DIR","uploads")
    base_url = current_app.config.get("STORAGE_BASE_URL","/files")
    os.makedirs(base, exist_ok=True)
    name = secure_filename(file_storage.filename) or "file.bin"
    key = f"{uuid.uuid4().hex}_{name}"
    path = os.path.join(base, key)
    file_storage.save(path)
    return f"{base_url}/{key}"

def s3_client():
    return boto3.client("s3",
        region_name=current_app.config.get("AWS_REGION"),
        aws_access_key_id=current_app.config.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=current_app.config.get("AWS_SECRET_ACCESS_KEY"),
    )

def presign_s3(key, content_type="application/octet-stream"):
    bucket = current_app.config.get("AWS_S3_BUCKET")
    client = s3_client()
    url = client.generate_presigned_url(
        "put_object",
        Params={"Bucket": bucket, "Key": key, "ContentType": content_type},
        ExpiresIn=3600
    )
    public_url = f"https://{bucket}.s3.{current_app.config.get('AWS_REGION')}.amazonaws.com/{key}"
    return url, public_url
