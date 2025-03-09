import base64
import hashlib
import json


class JWTManager(object):
    SECRET = None

    def __init__(self):
        pass

    def create(payload):
        header = json.dumps({'alg': 'HS256', 'typ': 'JWT'}).encode()
        payload = json.dumps(payload).encode()

        base64_header = base64.urlsafe_b64encode(header).decode().rstrip('=')
        base64_payload = base64.urlsafe_b64encode(payload).decode().rstrip('=')

        signature = hashlib.sha256(f'{base64_header}.{base64_payload}'.encode(
        ) + JWTManager.SECRET.encode()).digest()
        base64_signature = base64.urlsafe_b64encode(
            signature).decode().rstrip('=')

        return f'{base64_header}.{base64_payload}.{base64_signature}'

    def verify(token) -> bool:
        try:
            header, payload, signature = token.split('.')
            expected_signature = hashlib.sha256(
                f'{header}.{payload}'.encode() + JWTManager.SECRET.encode()).digest()
            base64_expected_signature = base64.urlsafe_b64encode(
                expected_signature).decode().rstrip('=')

            if signature != base64_expected_signature:
                return False
            return True
        except Exception as e:
            return False

    def decode(token):
        header, payload, signature = token.split('.')

        decoded_payload = base64.urlsafe_b64decode(payload + '==')
        payload_data = json.loads(decoded_payload)

        return payload_data

    def set_secret(secret):
        JWTManager.SECRET = secret
