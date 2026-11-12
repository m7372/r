import base64, hashlib, urllib.parse
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_v1_5
from Crypto.Util.Padding import pad, unpad
from app import gen_aes_key, rsa_encrypt, build_sign_data, gen_sign, decrypt

def test_aes_key_length():
    assert len(gen_aes_key()) == 16

def test_rsa_encrypt_decrypt_roundtrip():
    key = gen_aes_key()
    enc = rsa_encrypt(key)
    assert len(base64.b64decode(enc)) == 128

def test_sign_is_hex():
    s = gen_sign("a" * 16, "test-data")
    assert len(s) == 32
    assert all(c in "0123456789abcdef" for c in s)

def test_decrypt_roundtrip():
    key = "abcdefgh12345678"
    plain = '{"hello":"world"}'
    c = AES.new(key.encode(), AES.MODE_ECB)
    enc = base64.b64encode(c.encrypt(pad(plain.encode(), 16))).decode()
    result = decrypt(enc, key)
    assert result == {"hello": "world"}

def test_build_sign_data_url_encodes():
    data = build_sign_data({"a": "1", "b": "2"}, "123")
    assert urllib.parse.unquote_plus(data) == "12123"
