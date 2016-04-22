#!/usr/bin/env/python
import sys
from BitVector import *
import pprint
import os
AES_modulus = BitVector(bitstring='100011011')
subBytesTable = []                                                  # for encryption
invSubBytesTable = []                                               # for decryption
dos = BitVector(intVal = 2)
tres = BitVector(intVal = 3)#used for column mix
once = BitVector(intVal = 11)
catorce = BitVector(intVal = 14)
trece = BitVector(intVal = 13)
nueve = BitVector(intVal = 9)
Rcon = []
Rcon.append(BitVector(hexstring = "01000000"))
Rcon.append(BitVector(hexstring = "02000000"))
Rcon.append(BitVector(hexstring = "04000000"))
Rcon.append(BitVector(hexstring = "08000000"))
Rcon.append(BitVector(hexstring = "10000000"))
Rcon.append(BitVector(hexstring = "20000000"))
Rcon.append(BitVector(hexstring = "40000000"))
Rcon.append(BitVector(hexstring = "80000000"))
Rcon.append(BitVector(hexstring = "1b000000"))
Rcon.append(BitVector(hexstring = "36000000"))
modulus =BitVector(bitstring='100011011')


def genTables():
    c = BitVector(bitstring='01100011')
    d = BitVector(bitstring='00000101')
    for i in range(0, 256):
        # For the encryption SBox
        a = BitVector(intVal = i, size=8).gf_MI(AES_modulus, 8) if i != 0 else BitVector(intVal=0)
        # For byte scrambling for the encryption SBox entries:
        a1,a2,a3,a4 = [a.deep_copy() for x in range(4)]
        a ^= (a1 >> 4) ^ (a2 >> 5) ^ (a3 >> 6) ^ (a4 >> 7) ^ c
        subBytesTable.append(int(a))
        # For the decryption Sbox:
        b = BitVector(intVal = i, size=8)
        # For byte scrambling for the decryption SBox entries:
        b1,b2,b3 = [b.deep_copy() for x in range(3)]
        b = (b1 >> 2) ^ (b2 >> 5) ^ (b3 >> 7) ^ d
        check = b.gf_MI(AES_modulus, 8)
        b = check if isinstance(check, BitVector) else 0
        invSubBytesTable.append(int(b))

genTables()

#print "SBox for Encryption:"
#print subBytesTable
#print "\nSBox for Decryption:"
#print invSubBytesTable


def extract_round_key(): # round key 
    key = "howtogettosesame"
    key_bv = BitVector(textstring = key)
    #key_bv = BitVector(hexstring = "2b7e151628aed2a6abf7158809cf4f3c")
    key_arr = []
    key_arr.append(key_bv[0:32])
    key_arr.append(key_bv[32:64])
    key_arr.append(key_bv[64:96])
    key_arr.append(key_bv[96:128])
    ri = 0
    for i in range (0,37,4):
        #making G
        #rotation
        temp = key_arr[i+3].deep_copy()
        temp << 8
        star = 0
        finis = 8
        #substitution
        for k in range(0,4):
            val = temp[star:finis]
            [row, column] = val.divide_into_two()
            irow = int(row)
            icolumn = int(column)
            index = (irow*16) + icolumn
            tempint = BitVector(intVal = subBytesTable[index])
            largo = len(tempint)
            largo = 8 - largo
            tempint.pad_from_left(largo)
            temp[star:finis]  =tempint
            star= finis
            finis += 8
        g = Rcon[ri] ^ temp
        ri +=1
        #done making G
        key4 = key_arr[i] ^ g
        key5 = key4 ^ key_arr[i+1]
        key6 = key5 ^ key_arr[i+2]
        key7 = key6 ^ key_arr[i+3]
        key_arr.append(key4)
        key_arr.append(key5)        
        key_arr.append(key6)
        key_arr.append(key7)

    return key_arr


def print_arr(arr):
    for i in range(0,4):
        print arr[0][i].get_bitvector_in_hex(), arr[1][i].get_bitvector_in_hex(), arr[2][i].get_bitvector_in_hex(), arr[3][i].get_bitvector_in_hex()
    print ""



def encrypt_aes (input_file, output_file, llaves):
    #open file
    input_arr  =[[0 for x in range(4)] for x in range(4)]
    bv = BitVector( filename = input_file ) 
    FILEOUT = open( output_file, 'ab' ) 
    bv = BitVector( filename = input_file )
    tempv = [0]* 4
    
    while (bv.more_to_read ):
        bitvec = bv.read_bits_from_file( 128 ) 
        #bitvec = BitVector(hexstring = "3243f6a8885a308d313198a2e0370734")  
        leng = bitvec.length()                                        
        pad = 128 - leng
        bitvec.pad_from_right(pad)
        
        kv= 0
        start=0
        for i in range(0,4):
            for k in range(0,4):
                input_arr[i][k] = BitVector(size = 8)
                input_arr[i][k] =  bitvec[start:(start+8)]
                start +=8
        #finished construction of input array

        for i in range(0,4):
            input_arr[i][0] = input_arr[i][0] ^ llaves[i][0:8]
            input_arr[i][1] = input_arr[i][1] ^ llaves[i][8:16]
            input_arr[i][2] = input_arr[i][2] ^ llaves[i][16:24]
            input_arr[i][3] = input_arr[i][3] ^ llaves[i][24:32] 

        for ig in range(0,10):
            #lets do the substitution
            for i in range(0,4):
                for k in range(0,4):
                    [row, column] = input_arr[i][k].divide_into_two()
                    irow = int(row)
                    icolumn = int(column)
                    #print irow, icolumn
                    index = (irow*16) + icolumn
                    tempint = BitVector(intVal = subBytesTable[index])
                    largo = len(tempint)
                    largo = 8 - largo
                    tempint.pad_from_left(largo)
                    input_arr[i][k] = tempint
            #print_arr(input_arr)
            #2 shift rows
            for i in range(1,4):
                for k in range(0,4):
                    tempv[(k-i)%4] = input_arr[k][i]
                for k in range (0,4):
                    input_arr[k][i] = tempv[k]
            #print_arr(input_arr)
            #shift columns
            if(ig < 9):
                for i in range (0,4):
                    s0 = (dos.gf_multiply_modular(input_arr[i][0],modulus, 8)) ^ (tres.gf_multiply_modular(input_arr[i][1],modulus, 8)) ^ input_arr[i][2] ^ input_arr[i][3]
                    s1 = input_arr[i][0] ^ (dos.gf_multiply_modular(input_arr[i][1],modulus, 8)) ^ (tres.gf_multiply_modular(input_arr[i][2],modulus, 8)) ^ input_arr[i][3]
                    s2 = input_arr[i][0] ^ input_arr[i][1] ^ (dos.gf_multiply_modular(input_arr[i][2],modulus, 8)) ^ (tres.gf_multiply_modular(input_arr[i][3],modulus, 8))
                    s3 = (tres.gf_multiply_modular(input_arr[i][0],modulus, 8)) ^ input_arr[i][1] ^ input_arr[i][2] ^ (dos.gf_multiply_modular(input_arr[i][3],modulus, 8))
                    input_arr[i][0] = s0
                    input_arr[i][1] = s1
                    input_arr[i][2] = s2
                    input_arr[i][3] = s3
                #print_arr(input_arr)
                
            
        #xor key
            kv += 4   
            for i in range(0,4):
                input_arr[i][0] = input_arr[i][0] ^ llaves[kv+i][0:8]
                input_arr[i][1] = input_arr[i][1] ^ llaves[kv+i][8:16]
                input_arr[i][2] = input_arr[i][2] ^ llaves[kv+i][16:24]
                input_arr[i][3] = input_arr[i][3] ^ llaves[kv+i][24:32] 
        for i in range (0,4):
            #print_arr(input_arr)
            file_writebv = input_arr[i][0] + input_arr[i][1] + input_arr[i][2] + input_arr[i][3]
            file_writestuff = file_writebv
            file_writebv.write_to_file(FILEOUT) 






def dec_aes(input_file, output_file, llaves):
    #open file
    input_arr  =[[0 for x in range(4)] for x in range(4)]
    bv = BitVector( filename = input_file ) 
    FILEOUT = open( output_file, 'ab' ) 
    bv = BitVector( filename = input_file )
    tempv = [0]* 4
    while (bv.more_to_read ):
        bitvec = bv.read_bits_from_file( 128 )   
        leng = bitvec.length()                                        
        pad = 128 - leng
        bitvec.pad_from_right(pad)
        kv= 0
        start=0
        for i in range(0,4):
            for k in range(0,4):
                input_arr[i][k] = BitVector(size = 8)
                input_arr[i][k] =  bitvec[start:(start+8)]
                start +=8
        #finished construction of input array
        #print_arr(input_arr)
        llaves.reverse()
        #xor keys with "plain text"
        for i in range(0,4):
            input_arr[i][0] = input_arr[i][0] ^ llaves[i][0:8]
            input_arr[i][1] = input_arr[i][1] ^ llaves[i][8:16]
            input_arr[i][2] = input_arr[i][2] ^ llaves[i][16:24]
            input_arr[i][3] = input_arr[i][3] ^ llaves[i][24:32] 
      
        #print_arr(input_arr)

        for ig in range(0,10):
            #print ig
            #shift rows
            for i in range(1,4):
                for k in range(0,4):
                    tempv[(k+i)%4] = input_arr[k][i]
                for k in range (0,4):
                    input_arr[k][i] = tempv[k]
            #print_arr(input_arr)
            #lets do the substitution
            for i in range(0,4):
                for k in range(0,4):
                    [row, column] = input_arr[i][k].divide_into_two()
                    irow = int(row)
                    icolumn = int(column)
                    #print irow, icolumn
                    index = (irow*16) + icolumn
                    tempint = BitVector(intVal = invSubBytesTable[index])
                    largo = len(tempint)
                    largo = 8 - largo
                    tempint.pad_from_left(largo)
                    input_arr[i][k] = tempint
            #print_arr(input_arr)


            #xor key
            kv += 4   
            for i in range(0,4):
                input_arr[i][0] = input_arr[i][0] ^ llaves[kv+i][0:8]
                input_arr[i][1] = input_arr[i][1] ^ llaves[kv+i][8:16]
                input_arr[i][2] = input_arr[i][2] ^ llaves[kv+i][16:24]
                input_arr[i][3] = input_arr[i][3] ^ llaves[kv+i][24:32]

            #print_arr(input_arr)
            #shift columns
            if(ig > 0):
                for i in range (0,4):
                    s0 = (catorce.gf_multiply_modular(input_arr[i][0],modulus, 8)) ^ (once.gf_multiply_modular(input_arr[i][1],modulus, 8)) ^ (trece.gf_multiply_modular(input_arr[i][2],modulus, 8)) ^ (nueve.gf_multiply_modular(input_arr[i][3],modulus, 8))
                    s1 = (nueve.gf_multiply_modular(input_arr[i][0],modulus, 8)) ^ (catorce.gf_multiply_modular(input_arr[i][1],modulus, 8)) ^ (once.gf_multiply_modular(input_arr[i][2],modulus, 8)) ^ (trece.gf_multiply_modular(input_arr[i][3],modulus, 8))
                    s2 = (trece.gf_multiply_modular(input_arr[i][0],modulus, 8)) ^ (nueve.gf_multiply_modular(input_arr[i][1],modulus, 8)) ^ (catorce.gf_multiply_modular(input_arr[i][2],modulus, 8)) ^ (once.gf_multiply_modular(input_arr[i][3],modulus, 8))
                    s3 = (once.gf_multiply_modular(input_arr[i][0],modulus, 8)) ^ (trece.gf_multiply_modular(input_arr[i][1],modulus, 8)) ^ (nueve.gf_multiply_modular(input_arr[i][2],modulus, 8)) ^ (catorce.gf_multiply_modular(input_arr[i][3],modulus, 8))

                    input_arr[i][0] = s0
                    input_arr[i][1] = s1
                    input_arr[i][2] = s2
                    input_arr[i][3] = s3
            #print_arr(input_arr)
        for i in range (0,4):
            #print_arr(input_arr)
            file_writebv = input_arr[i][0] + input_arr[i][1] + input_arr[i][2] + input_arr[i][3]
            file_writestuff = file_writebv
            file_writebv.write_to_file(FILEOUT) 
if __name__ == "__main__":       
    keys = extract_round_key()
    if os.path.isfile('encryptedtext.txt'):
        os.remove('encryptedtext.txt')
    if os.path.isfile('decryptedtext.txt'):
        os.remove('decryptedtext.txt')
    encrypt_aes('plaintext.txt','encryptedtext.txt', keys)
    dec_aes('encryptedtext.txt','decryptedtext.txt', keys)
