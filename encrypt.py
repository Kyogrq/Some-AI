import base64
import hashlib
import numpy as np
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from sklearn.preprocessing import MinMaxScaler
from sklearn.neural_network import MLPRegressor

class UltimateEncrypter:
    def __init__(self, key):
        self.key = hashlib.sha512(key.encode()).digest()

    def encrypt_aes(self, data):
        backend = default_backend()
        iv = base64.b64encode(np.random.bytes(16))
        cipher = Cipher(algorithms.AES(self.key), modes.CFB(iv), backend=backend)
        encryptor = cipher.encryptor()
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(data.encode()) + padder.finalize()
        ct = encryptor.update(padded_data) + encryptor.finalize()
        return iv, ct

    def encrypt_ml(self, data):
        scaler = MinMaxScaler()
        X = np.array([ord(char) for char in data]).reshape(-1, 1)
        scaler.fit(X)
        X_scaled = scaler.transform(X)
        reg = MLPRegressor(hidden_layer_sizes=(100, 50), max_iter=2000, random_state=42)
        reg.fit(X_scaled, X_scaled)
        encrypted_data = reg.predict(X_scaled)
        return ''.join([chr(int(round(x[0]))) for x in scaler.inverse_transform(encrypted_data)])

    def transposition_cipher(self, plaintext, key):
        ciphertext = [''] * key
        for col in range(key):
            pointer = col
            while pointer < len(plaintext):
                ciphertext[col] += plaintext[pointer]
                pointer += key
        return ''.join(ciphertext)

key = input("Enter encryption key: ")
text = input("Enter text to encrypt: ")
encrypter = UltimateEncrypter(key)
iv, ct = encrypter.encrypt_aes(text)
print("AES IV:", iv.decode())
print("AES Ciphertext:", base64.b64encode(ct).decode())
encrypted_text = encrypter.encrypt_ml(text)
print("ML Encrypted Text:", encrypted_text)
transposition_encrypted_text = encrypter.transposition_cipher(text, len(key))
print("Transposition Encrypted Text:", transposition_encrypted_text)