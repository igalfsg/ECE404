#!/usr/bin/env/python
import sys
import pprint
import argparse
from PrimeGenerator import *
from BitVector import *
from flegmann_RSA_hw06 import *
from solve_pRoot import *

def arg_setup():
    #takes care of arguments in command line
    parser = argparse.ArgumentParser()
    parser.add_argument('inputfile')
    parser.add_argument('outputfile')
    args = parser.parse_args()
    return args


def create_keys():
    #creates the keys
    e = BitVector(intVal = 3)
    uno = BitVector(intVal = 1)
    tres = BitVector(intVal = 3)#used for checking the last two bits
    generator = PrimeGenerator( bits = 128, debug = 0 )
    p = BitVector(intVal = generator.findPrime())
    while (p[0:2] != tres and int (e.gcd(BitVector(intVal = int(p)-1))) != 1):
        p = BitVector(intVal = generator.findPrime())
    q = BitVector(intVal = generator.findPrime())
    while (q[0:2] != tres and int (e.gcd(BitVector(intVal = int(q)-1))) != 1 and p != q):
        q = BitVector(intVal = generator.findPrime())
    n = int(p) *int( q)
    n = BitVector(intVal = n)
    to = BitVector(intVal =((int(p)-1)*(int(q)-1)))
    d = e.multiplicative_inverse(to)
    priv = (d, n, p, q)
    pub = (e,n)
    return (pub, priv)

#takes 3 keys as tuples of two BitVectors and the filenames of the encrypted texts
#assumes 3 keys have same e values since it is one of the conditions for this algorithm to work

def Crack_RSA(key1, key2, key3, etext1, etext2, etext3, output_file):
    fin = BitVector(size = 0)
    e = key1[0]
    FILEOUT = open( output_file, 'a' ) 
    n1 =  key1[1]
    
    
    n2 =  key2[1]
    
    n3 =  key3[1]
    bigN = int(n1) * int(n2) * int (n3)
    bigN1 = BitVector (intVal = (bigN / int(n1)))
    bigN2 = BitVector (intVal = (bigN / int(n2)))
    bigN3 = BitVector (intVal = (bigN / int(n3)))
    mi1 = int(bigN1.multiplicative_inverse(n1))
    mi2 = int(bigN2.multiplicative_inverse(n2))
    mi3 = int(bigN3.multiplicative_inverse(n3))
    
    bv1 = BitVector(filename = etext1)
    bv2 = BitVector(filename = etext2)
    bv3 = BitVector(filename = etext3)
   
    while(bv1.more_to_read):
        bitvec1 = bv1.read_bits_from_file(256)
        bitvec2 = bv2.read_bits_from_file(256)
        bitvec3 = bv3.read_bits_from_file(256)
        
        temp = ((int(bitvec1) * int(bigN1) * mi1) + 
                (int(bitvec2) * int(bigN2) * mi2) +
                (int(bitvec3) * int(bigN3) * mi3)) % bigN
        
        temp2 = solve_pRoot(3, temp)
        temp = BitVector(intVal = temp2)
        pad = 128 - temp.length()
        temp.pad_from_left(pad)
        fin +=temp
    fin.write_to_file(FILEOUT)
    return


if __name__ == "__main__":
    argu = arg_setup()
    pub1, priv1 = create_keys()
    pub2, priv2 = create_keys()
    pub3, priv3 = create_keys()
    encrypt(argu.inputfile, "encry1.txt", pub1)
    encrypt(argu.inputfile, "encry2.txt", pub2)
    encrypt(argu.inputfile, "encry3.txt", pub3)
    Crack_RSA(pub1, pub2, pub3,"encry1.txt", "encry2.txt", "encry3.txt", argu.outputfile)
