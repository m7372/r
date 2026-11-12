import os, json, time, random, string, base64, hashlib, urllib.parse
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKCS1_v1_5
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

PUBLIC_RSA_KEY = "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCYo79ZFZHFCyboUBinm/I1OR7Obq2Do+4sMufINvD2Qw5fYvZeSYR24/lxRMsZnlbcP0a3/lG9dyX2G0ljvQwBSdCW9jTBBaOJiSW1M2DEFCP5/6ObJ7WCwDKxVVxebhzlzhGjjuPB86vsVVwYXTFtTZKfuTk3SQnpta/TOFE6cwIDAQAB"

app = Flask(__name__)
CORS(app)

def gen_aes_key():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(16))

def rsa_encrypt(key):
    pem = f"-----BEGIN PUBLIC KEY-----\n{PUBLIC_RSA_KEY}\n-----END PUBLIC KEY-----"
    c = Cipher_PKCS1_v1_5.new(RSA.import_key(pem))
    return base64.b64encode(c.encrypt(key.encode())).decode()

def build_sign_data(params, t):
    ks = sorted(params.keys())
    return urllib.parse.quote_plus("".join(str(params[k]) for k in ks if str(params[k])) + t)

def gen_sign(key, data):
    c = AES.new(key.encode(), AES.MODE_ECB)
    enc = c.encrypt(pad(data.encode(), AES.block_size))
    return hashlib.md5(base64.b64encode(enc)).hexdigest().lower()

def decrypt(b64, key):
    try:
        c = AES.new(key.encode(), AES.MODE_ECB)
        return json.loads(unpad(c.decrypt(base64.b64decode(b64)), AES.block_size))
    except Exception as e:
        return {"error": str(e)}

@app.get("/")
def health():
    return jsonify({"status": "ok", "service": "savita-backend"})

@app.post("/api/preview")
def preview():
    body = request.get_json(silent=True) or {}
    params = {
        'category': "0",
        'contentId': str(body.get("contentId", "15158")),
        'episodeId': str(body.get("episodeId", "86683")),
        'definition': str(body.get("definition", "GROOT_LD")),
        'projection': "false",
        'tryCode': "0"
    }
    t = str(int(time.time() * 1000))
    key = gen_aes_key()
    headers = {
        'User-Agent': "okhttp/4.12.0",
        'clienttype': "android_hitv0426",
        'versioncode': "133",
        'deviceid': "14335dd76714083d",
        'lang': str(body.get("lang", "ar")),
        'currenttime': t,
        'aeskey': rsa_encrypt(key),
        'sign': gen_sign(key, build_sign_data(params, t))
    }
    try:
        r = requests.get("https://mobile-api.hitv.ltd/savita/media/previewInfo",
                         params=params, headers=headers, timeout=20)
        j = r.json()
    except Exception as e:
        return jsonify({"error": str(e)}), 502

    if j.get("code") != "00000":
        return jsonify({"error": "upstream", "raw": j}), 400
    return jsonify({"success": True, "decrypted": decrypt(j["data"], key)})

@app.post("/api/request")
def generic():
    body = request.get_json(silent=True) or {}
    url = body.get("url", "")
    if not url.startswith("https://mobile-api.hitv.ltd/"):
        return jsonify({"error": "host blocked"}), 403
    try:
        r = requests.get(url, headers=body.get("headers", {}), timeout=20)
        return jsonify(r.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 502

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
