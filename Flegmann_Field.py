#!/usr/bin/env python

## FindMI.py

import sys

n = input("Enter Number for n: ")
 


def MI(num, mod):
    '''
    This function uses ordinary integer arithmetic implementation of the
    Extended Euclid's Algorithm to find the MI of the first-arg integer
    vis-a-vis the second-arg integer.
    '''
    NUM = num; MOD = mod
    x, x_old = 0L, 1L
    y, y_old = 1L, 0L
    while mod:
        q = num // mod
        num, mod = mod, num % mod
        x, x_old = x_old - q * x, x
        y, y_old = y_old - q * y, y
    if num != 1:
        return 6
    else:
        return 1


for i in range(2,n):
    vl = MI(i,n)
    if vl == 6:
        break
if vl == 6:
    print("Field")
else:
    print("Ring")
