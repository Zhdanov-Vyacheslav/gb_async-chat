import hashlib


def generate_hash(value: str, salt: bytes):
    return hashlib.pbkdf2_hmac('sha256', value.encode('utf-8'), salt, 100000)
