__author__ = 'x37liu'
from CM import AES_3GPP

class Cipher:
    def __init__(self ):
        self.cipher = AES_3GPP()

    def IP(self, key, count, direct, bearer, data):
        key = key.decode('hex')
        if direct == 'uplink':
            direct = 0
        else:
            direct = 1
        data = data.decode('hex')
        bitLen = len(data)*8
        return self.cipher.EIA2(key, count, bearer, direct, data, bitLen).encode('hex')

    def encrypt(self,key, count, direct, bearer, data):
        key = key.decode('hex')
        if direct == 'uplink':
            direct = 0
        else:
            direct = 1
        data = data.decode('hex')
        bitLen = len(data)*8
        return self.cipher.EEA2(key, count, bearer, direct, data, bitLen).encode('hex')

    def decrypt(self,key, count, direct, bearer, data):
        key = key.decode('hex')
        if direct == 'uplink':
            direct = 0
        else:
            direct = 1
        data = data.decode('hex')
        bitLen = len(data)*8
        return self.cipher.EEA2(key, count, bearer, direct, data, bitLen).encode('hex')

