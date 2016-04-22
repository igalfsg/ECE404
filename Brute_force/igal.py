#!/usr/bin/env python

###  DecryptForFun.py
###  Avi Kak  (kak@purdue.edu)
###  January 21, 2014, modified January 11, 2016

###  Medium strength encryption/decryption for secure message exchange
###  for fun.

###  Based on differential XORing of bit blocks.  Differential XORing
###  destroys any repetitive patterns in the messages to be ecrypted and
###  makes it more difficult to break encryption by statistical
###  analysis. Differential XORing needs an Initialization Vector that is
###  derived from a pass phrase in the script shown below.  The security
###  level of this script can be taken to full strength by using 3DES or
###  AES for encrypting the bit blocks produced by differential XORing.

###  Call syntax:
###
###        DecryptForFun.py  encrypted_file.txt  recover.txt
###
###  The decrypted output is deposited in the file `recover.txt'

import sys
import itertools
                                                     #(A)


for candidate in itertools.product('10', repeat=16):
    candidateu = "".join(candidate)
    print candidateu
    bv  =  BitVector(bitstring = candidateu)
    print bv
