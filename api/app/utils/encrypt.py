from cryptography.fernet import Fernet


class Encryption(object):
    KEY = None

    def __init__(self, key=None):
        Encryption.KEY = key

    def encrypt(self, value=None):
        if (value is None) or (value == ''):
            return ''

        if Encryption.KEY is None:
            raise ValueError('You must provide a non empty key')

        return Fernet(Encryption.KEY).encrypt(value.encode())

    def decrypt(self, value=None):
        if (value is None) or (value == ''):
            return ''

        if Encryption.KEY is None:
            raise ValueError('You must provide a non empty key')

        return Fernet(Encryption.KEY).decrypt(value).decode()
