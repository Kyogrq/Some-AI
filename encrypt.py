import base64
import hashlib
import numpy as np
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from sklearn.preprocessing import MinMaxScaler
from sklearn.neural_network import MLPRegressor

class UltimateDecrypter:
    def __init__(self, key):
        self.key = hashlib.sha512(key.encode()).digest()

    def decrypt_aes(self, iv, ct):
        backend = default_backend()
        iv = base64.b64decode(iv)
        cipher = Cipher(algorithms.AES(self.key), modes.CFB(iv), backend=backend)
        decryptor = cipher.decryptor()
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        pt = unpadder.update(decryptor.update(ct)) + unpadder.finalize()
        return pt.decode('utf-8')

    def decrypt_ml(self, encrypted_data):
        scaler = MinMaxScaler()
        X = np.array([ord(char) for char in encrypted_data]).reshape(-1, 1)
        scaler.fit(X)
        X_scaled = scaler.transform(X)
        reg = MLPRegressor(hidden_layer_sizes=(100, 50), max_iter=2000, random_state=42)
        reg.fit(X_scaled, X_scaled)
        decrypted_data = reg.predict(X_scaled)
        return ''.join([chr(int(round(x[0]))) for x in scaler.inverse_transform(decrypted_data)])

    def transposition_decipher(self, ciphertext, key):
        num_of_columns = int(np.ceil(len(ciphertext) / key))
        num_of_rows = key
        num_of_shaded_boxes = (num_of_columns * num_of_rows) - len(ciphertext)
        plaintext = [''] * num_of_columns
        col = 0
        row = 0
        for symbol in ciphertext:
            plaintext[col] += symbol
            col += 1
            if (col == num_of_columns) or (col == num_of_columns - 1 and row >= num_of_rows - num_of_shaded_boxes):
                col = 0
                row += 1
        return ''.join(plaintext)

key = input("Enter decryption key: ")
iv = input("Enter AES IV: ")
ct = base64.b64decode(input("Enter AES Ciphertext: "))
decrypter = UltimateDecrypter(key)
aes_decrypted_text = decrypter.decrypt_aes(iv, ct)
print("AES Decrypted Text:", aes_decrypted_text)
encrypted_text = input("Enter ML Encrypted Text: ")
ml_decrypted_text = decrypter.decrypt_ml(encrypted_text)
print("ML Decrypted Text:", ml_decrypted_text)
transposition_encrypted_text = input("Enter Transposition Encrypted Text: ")
transposition_decrypted_text = decrypter.transposition_decipher(transposition_encrypted_text, len(key))
print("Transposition Decrypted Text:", transposition_decrypted_text)