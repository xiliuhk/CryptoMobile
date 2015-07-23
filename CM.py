# −*− coding: UTF−8 −*−
#/**
# * Software Name : CryptoMobile 
# * Version : 0.1.0
# *
# * Copyright © 2013. Benoit Michau. ANSSI.
# *
# * This program is free software: you can redistribute it and/or modify
# * it under the terms of the GNU General Public License version 2 as published
# * by the Free Software Foundation. 
# *
# * This program is distributed in the hope that it will be useful,
# * but WITHOUT ANY WARRANTY; without even the implied warranty of
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# * GNU General Public License for more details. 
# *
# * You will find a copy of the terms and conditions of the GNU General Public
# * License version 2 in the "license.txt" file or
# * see http://www.gnu.org/licenses/ or write to the Free Software Foundation,
# * Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA
# *
# *--------------------------------------------------------
# * File Name : CryptoMobile/CM.py
# * Created : 2013-07-13
# * Authors : Benoit Michau 
# *--------------------------------------------------------
#*/

########################################################
# CryptoMobile python toolkit
#
# Interfaces C implementation of reference mobile cryptographic algorithms 
# to python primitives
# WARNING: mobile crypto algorithms specifications are freely available on the web, 
# but generally require license to be used in field equipments
#
# C source code from 3GPP / ETSI / GSMA / NIST web pages:
# - Kasumi (UEA1, UIA1)
# - SNOW3G (UEA2, UIA2, EEA1, EIA1)
# - ZUC (EEA3, EIA3)
# - AES (EEA2, EIA2) - from pycrypto
#######################################################

import os
import sys
from math import ceil
from struct import pack, unpack
from binascii import hexlify, unhexlify
from ctypes import *

#AES CTR and ECB modes for LTE crypto are imported from pycrypto
#AES CMAC mode is implemented here from AES ECB
try:
    from Crypto.Cipher import AES
    # filter * export
    __all__ = ['CryMo', 'AES_3GPP',
               'EEA2', 'EIA2']
    with_pycrypto = True
except ImportError:
    print('[WNG] [Import] Crypto.Cipher.AES from pycrypto not found\n' \
           '[-] EEA2 / EIA2 not available')
    # filter * export
    __all__ = ['CryMo',
               'UEA2', 'UIA2',
              ]
    with_pycrypto = False


# convinience functions: change their content if you want
def log(level='DBG', msg=''):
    # log wrapper
    print('[%s] %s' % (level, msg))

# class and exception wrapper for all crypto-mobile algorithms
class CryMo(object):
    pass

class CMException(Exception):
    pass
    

###
# python wrapper to pycrypto AES
###
#
AES_key_size = 16
AES_block_size = 16
if with_pycrypto:
    # Initialize pycrypto AES block cipher constants
    AES.key_size = AES_key_size
    AES.block_size = AES_block_size
    aes_ecb = lambda key, data: AES.new(key, AES.MODE_ECB).encrypt(data)
#
xor_str = lambda a, b: ''.join(map(chr, [ord(a[i])^ord(b[i]) for i in \
                               range(min(len(a), len(b)))] ))
_pow64 = 0x10000000000000000

# Define a class for AES_CTR and AES_CMAC as specified in TS 33.401
# AES_CMAC is defined in NIST 800-38B
class AES_3GPP(CryMo):
    '''
    LTE 2nd encryption / integrity protection algorithm
    It is AES-based, working with:
        - 128 bits key and 128 bits block
        - in CTR mode for ciphering (based on pycrypto function)
        - in CMAC mode for integrity protection 
          (made from pycrypto AES-ECB function)
    
    Generator initialization and keystream generation primitives are defined in
    .AES_CMAC(K, M, Tlen, Mlen) -> MAC
        K: 16 bytes key
        M: message to MAC
        Tlen: MAC length expected (between 1 and 128 bits)
        Mlen: message length in bits (in case not byte aligned)
        MAC: produced MAC, compliant to Tlen length in bits
    
    LTE mode of operation (EEA2, EIA2)
    For ciphering messages at LTE PDCP and NAS layer:
    .EEA2(key, count, bearer, dir, data_in, bitlen) -> data_out
        key is 16 bytes string
        count is uint32 integer (or long, as it is the way python works)
        bearer is unsigned integer limited to LTE bearers (coded on 5 bits)
        dir is 0 or 1 integer depending on uploading or downloading
        data_in is a variable-length string, to be ciphered / deciphered
        bitlen is an integer, representing the length of data_in in bits
            optional to pass, depending if data_in is byte aligned
        data_out is the result of ciperhing / deciphering
    For producing MAC-I integrity code for LTE RRC and NAS messages:
    .EIA2(key, count, fresh, dir, data_in, bitlen) -> mac
        key is 16 bytes string
        count is uint32 integer
        bearer is unsigned integer limited to LTE bearers (coded on 5 bits)
        dir is 0 or 1 integer depending on uploading or downloading
        data_in is a variable-length string, to use for MAC computing
        bitlen is uint64 integer, representing the length of data_in in bits
            optional to pass, depending if data_in is byte aligned
        mac is a 4 bytes string
    '''
    
    dbg_cmac = 0
    
    def __counter(self):
        if not hasattr(self, 'ctr_count'):
            self.ctr_count = 0
        else:
            self.ctr_count += 1
            if self.ctr_count == _pow64:
                self.ctr_count = 0
        cnt = ''.join((self.iv_64h, pack('!Q', self.ctr_count)))
        #print hexlify(cnt)
        return cnt
    
    def __cmac_key_sched(self, key):
        # schedule the key for potential padding
        # AES a zero input block
        L = aes_ecb(key, 16*'\0')
        if self.dbg_cmac:
            print('L: %s' % hexlify(L))
        # schedule depending of the MSB of L
        # python-fu: unpack the 128 bits register as 2 BE uint64
        Lh, Ll = unpack('!QQ', L)
        # sum both uint64 as an uint128, left-shift and filter
        K1 = (((Lh*_pow64)+Ll) << 1) & 0xffffffffffffffffffffffffffffffff
        # XOR K1 depending of the MSB of L
        if Lh & 0x8000000000000000:
             K1 ^= 0x87
        # re-shift K1 to make K2
        K2 = (K1 << 1) & 0xffffffffffffffffffffffffffffffff
        # XOR K2 depending of the MSB of K1
        if K1 & 0x80000000000000000000000000000000:
            K2 ^= 0x87
        # return 2 corresponding 16-bytes strings K1, K2
        return pack('!QQ', K1/_pow64, K1%_pow64), \
               pack('!QQ', K2/_pow64, K2%_pow64)
    
    def AES_CMAC(self, K=16*'\0', M='', Tlen=AES_block_size*8, Mlen=None):
        # prepare bit length
        if not isinstance(Mlen, (int, long)) or Mlen < 0 or Mlen > len(M)*8:
            Mlen = len(M)*8
        # truncate / zero the message if Mlen is given correctly
        else:
            M = M[:int(ceil(Mlen/8.0))]
            lastbits = (8-(Mlen%8))%8
            if lastbits:
                M = ''.join((M[:-1], \
                    chr(ord(M[-1:]) & (0x100 - (1<<lastbits))) ))
        # define parameters for iterating
        b = AES_block_size*8
        # n is useless, as we iterate directly over Mlist:
        #n = int(ceil(Mlen / float(b))) if Mlen else 1
        # K1, K2 subkeys
        K1, K2 = self.__cmac_key_sched(K)
        if self.dbg_cmac:
            print('K1: %s' % hexlify(K1))
            print('K2: %s' % hexlify(K2))
        # message divided into blocks of length b, and last Mn taken out
        Mlist = [M[i:i+AES_block_size] \
                 for i in range(0, int(ceil(Mlen/8.0)), AES_block_size)]
        #print Mlist
        if Mlist:
            Mn = Mlist.pop()
            Mnlen = Mlen % b
            # adjust last block depending of its length
            if Mnlen:
                # if M not AES blocksize-aligned:
                # NIST'way to pad: (Mn*||10^j)^K2, j = n*b-Mlen-1 ...
                # so... 1st, pad with 0
                Mn += '\0' * (16-int(ceil(Mnlen/8.0)))
                # then switch the 1st padding bit to 1 
                # in the 1st byte with padding
                pad_offset = Mnlen/8
                Mn = ''.join(( \
                    Mn[:pad_offset],
                    chr( ord(Mn[pad_offset]) + (1 << (8-((Mnlen%8)+1))) ), \
                    Mn[pad_offset+1:] ))
                #print('Mn padded: %s' % hexlify(Mn))
                # XOR Mn with subkey
                Mn = xor_str(Mn, K2)
            else:
                # if M is AES blocksize-aligned, XOR Mn with subkey:
                Mn = xor_str(Mn, K1)
        else:
            # this is for the NIST cra$*?* test vectors...
            Mn = '\x80\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0'
            Mn = xor_str(Mn, K2)
        Mlist.append(Mn)
        # loop over the message to MAC it
        C = AES_block_size * '\0'
        for Mi in Mlist:
            #print('Mi: %s' % hexlify(Mi))
            C = aes_ecb(K, xor_str(C, Mi))
        # if Tlen not byte-aligned, zero out last bits of T
        T = C[:int(ceil(Tlen/8.0))]
        if Tlen%8:
            T = ''.join((T[:-1], chr(ord(T[-1])&(0xff-(1<<(8-(Tlen%8))-1)))))
        return T
    
    def EEA2(self, key=16*'\0', count=0, bearer=0, dir=0, data='', bitlen=None):
        max32 = pow(2, 32)
        length = len(data)
        # args sanity check
        if not isinstance(key, str) or len(key) != 16:
            raise(CMException)
        if not isinstance(count, (int, long)) or count < 0 or count >= max32:
            raise(CMException)
        if not isinstance(bearer, int) or bearer < 0 or bearer >= 32:
            raise(CMException)
        if not isinstance(dir, int) or dir not in (0, 1):
            raise(CMException)
        if not isinstance(data, str) or length >= 16777216:
            raise(CMException)
        if not isinstance(bitlen, int) or bitlen < 0 or bitlen > length*8:
            bitlen = length*8
        # if bitlen is given correctly, truncate data if needed
        else:
            data = data[:int(ceil(bitlen/8.0))]
        # build IV with highest 64 bits of the CTR counter
        self.iv_64h = pack('!II', count, (bearer<<27)+(dir<<26))
        # initialize CTR counter
        self.ctr_count = -1
        ciph = AES.new(key, AES.MODE_CTR, counter=self.__counter).encrypt(data)
        # zero out last bits of data if needed
        lastbits = (8-(bitlen%8))%8
        if lastbits:
            ciph = ''.join((ciph[:-1], \
                      chr(ord(ciph[-1:]) & (0x100 - (1<<lastbits))) ))
        return ciph
    
    def EIA2(self, key=16*'\0', count=0, bearer=0, dir=0, data='', bitlen=None):
        max32 = pow(2, 32)
        length = len(data)
        # args sanity check
        if not isinstance(key, str) or len(key) != 16:
            print isinstance(key, str)
            print len(key)
            raise(CMException)
        if not isinstance(count, (int, long)) or count < 0 or count >= max32:
            raise(CMException)
        if not isinstance(bearer, int) or bearer < 0 or bearer >= 32:
            raise(CMException)
        if not isinstance(dir, int) or dir not in (0, 1):
            raise(CMException)
        if not isinstance(data, str) or length >= 16777216:
            raise(CMException)
        if not isinstance(bitlen, int) or bitlen < 0 or bitlen > length*8:
            bitlen = length*8
        # prepare concatenated message:
        M = ''.join(( pack('!II', count, (bearer<<27)+(dir<<26)), data))
        return self.AES_CMAC(key, M, 32, bitlen+64)

    
#
###################
# DEFINE 3GPP ALG #
# convinient for  #
# python export   #
###################
#
if with_pycrypto:
    A = AES_3GPP()
if with_pycrypto:
    EEA2 = A.EEA2
    EIA2 = A.EIA2
#
