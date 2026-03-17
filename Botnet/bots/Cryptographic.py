import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# Encrypt and decrypt data using Fernet symmetric encryption
class Cryptographic:
    def __init__(self):
        self.psswd = b"my_secret_password"
        self.salt = b'some_constant_salt'
        self.kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
        )
        self.key = base64.urlsafe_b64encode(self.kdf.derive(self.psswd))
        self.f = Fernet(self.key)

    def encrypt(self, data):
        return self.f.encrypt(data.encode())

    def decrypt(self, data):
        return self.f.decrypt(data.decode())