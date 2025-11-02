from ..models.wifi import WifiAccessPoint

def estimate_location(readings):
    if not readings: return None, None
    bssids = [r.get("bssid") for r in readings if r.get("bssid")]
    if not bssids: return None, None
    aps = {ap.bssid: ap for ap in WifiAccessPoint.query.filter(WifiAccessPoint.bssid.in_(bssids)).all()}
    weighted = []
    for r in readings:
        ap = aps.get(r.get("bssid")); 
        if not ap or ap.lat is None or ap.lon is None: continue
        rssi = r.get("rssi", -90); weight = max(1, 100 + rssi)  # RSSI negativo → peso menor
        weighted.append((ap.lat, ap.lon, weight))
    if not weighted: return None, None
    sw = sum(w for _,_,w in weighted)
    lat = sum(lat*w for lat,_,w in weighted)/sw
    lon = sum(lon*w for _,lon,w in weighted)/sw
    return lat, lon
