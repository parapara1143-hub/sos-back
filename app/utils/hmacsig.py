
import hmac, hashlib, time
from flask import request, abort
from ..config import Config

def verify_hmac():
    secret = (Config().INTEGRATION_SECRET or "").encode("utf-8")
    sig = request.headers.get("X-Signature")
    ts = request.headers.get("X-Timestamp")
    idem = request.headers.get("X-Idempotency-Key")
    if not sig or not ts or not idem:
        abort(401)
    try:
        ts_i = int(ts)
    except Exception:
        abort(401)
    if abs(int(time.time()) - ts_i) > 300:
        abort(401)  # 5 min window
    raw = request.get_data() or b""
    base = (ts + ":" + idem).encode("utf-8") + b"." + raw
    calc = hmac.new(secret, base, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(calc, sig):
        abort(401)
