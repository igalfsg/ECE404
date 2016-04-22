#!/usr/bin/env/python
import sys
import pprint
import argparse
from PrimeGenerator import *
from BitVector import *


def create_keys():
    #creates the keys
    e = BitVector(intVal = 65537)
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
    d = int(d)
    e = int (e)
    n = int (n)
    p = int (p)
    q = int (q)
    with open('private_key.txt', 'w') as f :
    	f.write(str(d)+"\n")
    	f.write(str(n)+"\n")
    	f.write(str(p)+"\n")
    	f.write(str(q)+"\n")

    with open('public_key.txt', 'w') as f:
    	f.write(str(e)+"\n")
    	f.write(str(n)+"\n")
create_keys()
