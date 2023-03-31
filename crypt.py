import hashlib
import os
import base64

from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Util.Padding import pad, unpad


class AESCipher(object):

    def __init__(self, key: str):
        #self.bs = 32
        self.key = hashlib.sha256(key.encode('utf-8')).digest() #turns the password into a 32char long key

    def pad(self, s):
        return pad(s,16)

    def remove_pad(self, m):
        return unpad(m,16)
        
        #encrypts plaintext and generates IV (initialization vector)
    def encrypt(self, plaintext):
        plaintext = self.pad(plaintext)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return iv + cipher.encrypt(plaintext)

        #derypts ciphertexts
    def decrypt(self, ciphertext):
        iv = ciphertext[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        plaintext = cipher.decrypt(ciphertext[AES.block_size:])
        return self.remove_pad(plaintext)
    
        #encrypts a file and returns a comment to be posted
    def encrypt_file(self, file_path):

        with open(file_path, 'rb') as fo:
            plaintext = fo.read()
        enc = self.encrypt(plaintext)
        comment = base64.b64encode(enc)
        #comment = enc.decode('ISO-8859-1').encode('ascii')
        return comment 
        
        #takes in a comment to be posted and decrypts it into a file
    def decrypt_file(self, comment, file_path):

        ciphertext = base64.b64decode(comment)
        #ciphertext = comment.decode('ascii').encode('ISO-8859-1')
        dec = self.decrypt(ciphertext)
        with open(file_path, 'wb') as fo:
            fo.write(dec)

