import sys
import DES_flegmann
import os
import random
from BitVector import *
# Expansion permutation (See Section 3.3.1):
expansion_permutation = [31, 0, 1, 2, 3, 4, 3, 4, 5, 6, 7, 8, 7, 8, 
9, 10, 11, 12, 11, 12, 13, 14, 15, 16, 15, 16, 17, 18, 19, 20, 19, 
20, 21, 22, 23, 24, 23, 24, 25, 26, 27, 28, 27, 28, 29, 30, 31, 0]

# P-Box permutation (the last step of the Feistel function in Figure 4):
p_box_permutation = [15,6,19,20,28,11,27,16,0,14,22,25,4,17,30,9,
1,7,23,13,31,26,2,8,18,12,29,5,21,10,3,24]

def checkdiff (file1, file2):
    bv1 = BitVector(filename = file1)
    bv2 = BitVector(filename = file2)
    cuenta = 0
    while (bv1.more_to_read):
        bitv1 = bv1.read_bits_from_file( 64 )
        bitv2 = bv2.read_bits_from_file( 64 )
        xorthi = bitv1 ^ bitv2
        for i in range(64):
            if xorthi[i] == 1:
                cuenta = cuenta + 1
        return cuenta


def messwithfile(rightf, messedf):
    FILEOUT = open (messedf, 'wb')
    lakey = DES_flegmann.get_encryption_key()
    round_keys = DES_flegmann.extract_round_key(lakey)
    tamano = os.path.getsize(rightf)
    tamano = tamano / 8
    bv = BitVector(filename = rightf)
    count = 0
    tot = 0
    for index in range(8):
        while (bv.more_to_read):
            bitvec = bv.read_bits_from_file( 64 ) 
            leng = bitvec.length()              
            pad = 64 - leng
            if count == index:
                bitvec.pad_from_right(pad)
                bitvec[random.randint(0,15)] ^= 1
                bitvec.write_to_file(FILEOUT)
            count = count + 1
        FILEOUT.close()
        bv.close_file_object()
        DES_flegmann.des(1, rightf, 'righte.txt',round_keys)
        DES_flegmann.des(1, messedf, 'messede.txt', round_keys)
        tot += checkdiff('righte.txt', 'messede.txt')
        os.remove('righte.txt')
        os.remove('messede.txt')
    return tot / 8
def createsb():
    row1 = []
    row2 = []
    row3 = []
    row4 = []
    sb = []
    sbs = []
    for k in range(8):
        for i in range(16):
        #rnum = random.randint(0,15)
            row1.append(random.randint(0,15))
            row2.append(random.randint(0,15))
            row3.append(random.randint(0,15))
            row4.append(random.randint(0,15))
        sb.append(row1)
        sb.append(row2)
        sb.append(row3)
        sb.append(row4)
        sbs.append(sb)
        row1 = []
        row2 = []
        row3 = []
        row4 = []
        sb = []
    return sbs


def des( s_box, input_file, output_file, keys ): 
    FILEOUT = open( output_file, 'ab' ) 
    bv = BitVector( filename = input_file )
    while (bv.more_to_read ):
        bitvec = bv.read_bits_from_file( 64 )   ## assumes that your file has an integral
        leng = bitvec.length()                                        ## multiple of 8 bytes. If not, you must pad it.
        pad = 64 - leng
        bitvec.pad_from_right(pad)
        [LE, RE] = bitvec.divide_into_two()   
        for i in range(16):        
            righty = RE.permute(expansion_permutation)
            resultxor = righty ^ keys[i]
            #s substitution
            temp_bv = BitVector(size = 6)
            row_bv = BitVector(size = 2)
            col_bv = BitVector(size = 4)
            ini=0
            fin=6
            inf=0
            fif=4
            final_bv = BitVector(size = 32)
            for k in range(8):
                temp_bv = resultxor[ini:fin]
                row_bv[0:1] = temp_bv[0:1]
                row_bv[1:2] = temp_bv[5:6]
                col_bv = temp_bv[1:5]
                row = row_bv.int_val()#get row
                col = col_bv.int_val()#get column      
                    #get stuff from sbox 
                newd = s_box[k][row][col]
                temp = BitVector(intVal = newd)
                temp_leng = temp.length()
                lpad = 4 - temp_leng
                temp.pad_from_left(lpad)
                final_bv[inf:fif] = temp
                inf = inf + 4
                fif = fif + 4
                ini = ini + 6#increase to the next thing
                fin = fin + 6#increase to th next chunck
                #permutation with p box
            last_p = final_bv.permute(p_box_permutation)
                #xor with le result = RE
            temporal = RE
            RE = last_p ^ LE
            LE = temporal #le equals old re     
            #for loop done
            #put left + right on output file
        file_writebv =  RE + LE
        file_writebv.write_to_file(FILEOUT)


if __name__ == "__main__":
    print "question 1 answer:"
    print messwithfile('message.txt','nuevo.txt')#check quiestion1
    os.remove('nuevo.txt')


    print "question 2 answer:"
    lakey = DES_flegmann.get_encryption_key()
    round_keys = DES_flegmann.extract_round_key(lakey)
    sbox = createsb()
    des(sbox, 'message.txt', 'sb.txt', round_keys)
    sbor = checkdiff ('encrypted.txt', 'sb.txt')
    sbox = createsb()
    des(sbox, 'message.txt', 'sb1.txt', round_keys)
    sbor1 = checkdiff ('encrypted.txt', 'sb1.txt')
    print "first Sbox change: ", sbor, "second sbox change: ", sbor1
    avg = (sbor + sbor1) / 2
    print "average sbox change: ", avg
    os.remove('sb.txt')

    print "question 3 answer:"
    os.remove('sb1.txt')
    changes = 0
    for j in range (4):
        indexc = random.randint(0,40)
        lakey[indexc] = lakey[indexc]^1 #change a random bit on key
        round_keys = DES_flegmann.extract_round_key(lakey)
        DES_flegmann.des(1, 'message.txt', 'encryptedwrongk.txt', round_keys)
        changes += checkdiff ('encrypted.txt', 'encryptedwrongk.txt')
        os.remove('encryptedwrongk.txt')
    print changes
