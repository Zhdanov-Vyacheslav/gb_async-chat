import hashlib


def generate_hash(value: str, salt: bytes):
    return hashlib.pbkdf2_hmac('sha256', valueG.encode('utf-8'), salt, 100000)
