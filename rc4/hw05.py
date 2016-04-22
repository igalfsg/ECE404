#!/usr/bin/env/python
import sys
import pprint

from copy import deepcopy
class RC4 :



    def __init__(self, key) :
        self.S = self.generate_S(key)
    def generate_S(self, key):
        s = []
        t = []
        for i in range (0, 256):
            s.append(i)
            t.append(key[i % (len(key))])
        j = 0
        for i in range (0,256):
            j = (j + s[i] +ord(t[i])) % 256
            s[i], s[j] = s[j], s[i]
        return s
    

    def encrypt (self, data):
        i = 0
        j = 0
        final_data = ""
        S = deepcopy(self.S)
        for byte in data:
            i = ( i + 1 ) % 256
            j = ( j + S[i] ) % 256
            S[i], S[j] = S[j], S[i]
            k = ( S[i] + S[j] ) % 256
            final_data += chr( ord(byte) ^ S[k] )
        return final_data

    def decrypt (self, data):
        i = 0
        j = 0
        final_data = ""
        S = deepcopy(self.S)
        for byte in data:
            i = ( i + 1 ) % 256
            j = ( j + S[i] ) % 256
            S[i], S[j] = S[j], S[i]
            k = ( S[i] + S[j] ) % 256
            final_data += chr( ord(byte) ^ S[k] )
        return final_data


def get_data(file_name):
    
    header = []

    with open (file_name, 'rb') as input_data:
        for i in range (0,3):
            header.append(input_data.readline())
        rest = input_data.read()

    return (rest, header)

if __name__ == "__main__": 
    test = RC4("Igalinsoy")
    pic, header = get_data("winterTown.ppm")
    encrypted = test.encrypt(pic)
    decrypted = test.decrypt(encrypted)
    if pic == decrypted:
        print "yay"
    else:
        print "upsie"
#this program had to prove that the encyption of the image worked the header was taken care by the person using the encryption
