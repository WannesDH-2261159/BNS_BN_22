import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


password = b"my_secret_password"
salt = b'some_constant_salt' # Should be unique/random
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=100000,
)
key = base64.urlsafe_b64encode(kdf.derive(password))
f = Fernet(key)



encrypted = "gAAAAABpuS5IVbM5RlIDShydPzm3eyjMgDfTcqW4I4EkZ-_EmwN2QLZ4aDgialhefgyn-moQjr7DDZ048YK-KRCDPk7v4dAf9Epjd79DBXMYA9yFI8KAO3U=".encode()
print("Encrypted: " + encrypted.decode())

decrypted = f.decrypt(encrypted).decode()
print("result: " + decrypted)