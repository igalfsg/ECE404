#!/usr/bin/env/python
import sys
import pprint
import argparse
from PrimeGenerator import *
from BitVector import *

def arg_setup():
    #takes care of arguments in command line
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', action='store_true')
    parser.add_argument('-e', action='store_true')
    parser.add_argument('inputfile')
    parser.add_argument('outputfile')
    args = parser.parse_args()
    return args




def create_keys():
    #creates the keys
    with open('private_key.txt', 'r') as f:
        d = f.readline()
        n = f.readline()
        p = f.readline()
        q = f.readline()
    d = BitVector(intVal = int(d))
    n = BitVector(intVal = int(n))
    p = BitVector(intVal = int(p))
    q = BitVector(intVal = int(q))
    with open('public_key.txt', 'r') as f:
        e = f.readline()
        n = f.readline()
    e = BitVector(intVal = int(e))
    n = BitVector(intVal = int(n))
    priv = (d, n, p, q)
    pub = (e,n)
    return(pub, priv)


def find_exponent(block, d, pq) :
    res = 1
    while ( d > 0 ) :
        if ( d & 1 ) :
            res = ( res * block ) % pq
        d = d>>1
        block = ( block * block ) % pq
    return res

def Chinese_magic(blok, d, n, p, q):
    Vq = find_exponent(int(blok), int(d), int(q))
    Vp = find_exponent(int(blok), int(d), int(p))
    n1 = int(n) / int(p)
    n2 = int(n) / int(q)

    n1_bv = BitVector(intVal = n1)
    n2_bv = BitVector(intVal = n2)

    n1_MI = int(n1_bv.multiplicative_inverse(p))
    n2_MI = int(n2_bv.multiplicative_inverse(q))
    
    Xp = int(q) * n1_MI
    Xq = int(p) * n2_MI
    magic_num = ((Vp * Xp) + (Vq*Xq)) % int(n)

    return magic_num


def decrypt(input_file, output_file, key):
    d = key[0]
    FILEOUT = open( output_file, 'ab' ) 
    n = key[1]
    p = key[2]
    q = key[3]
    result_bv = BitVector(size =0) #used to append the results
    bv = BitVector(filename = input_file)
    while(bv.more_to_read):
        bitvec = bv.read_bits_from_file(256)
        dec = Chinese_magic(bitvec, d, n, p, q)
        pad = 128 - BitVector(intVal =dec).length()
        result_bv += BitVector(intVal =dec, size  = 128 )
        
    result_bv.write_to_file(FILEOUT)

def encrypt (input_file, output_file, key):
    e = key[0]
    FILEOUT = open( output_file, 'a' ) 
    n = key[1]
    result_bv = BitVector(size =0) #used to append the results
    bv = BitVector(filename = input_file)
    while(bv.more_to_read):
        bitvec = bv.read_bits_from_file(128)
        leng = bitvec.length()                                      
        pad = 128 - leng
        bitvec.pad_from_right(pad)
        bitvec.pad_from_left(128)
        
        temp = find_exponent(int(bitvec), int(e),int(n))
        temp  = BitVector(intVal = temp)
        pad = 256 -  temp.length()
        temp.pad_from_left(pad)
        result_bv += temp
    result_bv.write_to_file(FILEOUT)
 
if __name__ == "__main__":
    argumentos = arg_setup()
    pub, priv =create_keys()
    if(argumentos.d):
        decrypt(argumentos.inputfile, argumentos.outputfile, priv)
    elif(argumentos.e):
        encrypt(argumentos.inputfile, argumentos.outputfile, pub)
