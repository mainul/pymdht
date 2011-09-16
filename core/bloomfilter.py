# Copyright (C) 2011 Md. Mainul Hossain
# Released under GNU LGPL 2.1
# See LICENSE.txt for more information

import socket
from hashlib import sha1
import math


K = 2
M = 256 * 8

class BloomFilter(object):

    def __init__(self, bloom=None):
        self.bloom = bloom or '\0' * (M / 8)
        
    
    def insert_ip(self, ip):
        family = socket.getaddrinfo(ip, socket.AF_INET)
        
        if family[0][0] == 2:
            bin_ip = socket.inet_pton(socket.AF_INET, ip)
        elif family[0][0] == 10:
            bin_ip = socket.inet_pton(socket.AF_INET6, ip)
        
        hashed_ip = sha1(bin_ip).digest()
                
        index1 = ord(hashed_ip[0]) | (ord(hashed_ip[1]) << 8)
        index2 = ord(hashed_ip[2]) | (ord(hashed_ip[3]) << 8)
        
        index1 %= M
        index2 %= M
        
        self.bloom = self.bloom[:index1/8] + chr(ord(self.bloom[index1/8]) | (1 << (index1 % 8))) + self.bloom[index1/8+1:]
        self.bloom = self.bloom[:index2/8] + chr(ord(self.bloom[index2/8]) | (1 << (index2 % 8))) + self.bloom[index2/8+1:]
        
        return self.bloom
        
    
    def hex_repr(self):
    	return ' ' .join(['%X' %ord(i) for i in self.bloom]).strip()
     
    
    def count_zero_bits(self):
    	self.counter = 0
    	for byte in self.bloom:
    	    mask = 1
    	    while (mask != 256):
                bits = ord(byte) & mask    
                if bits == 0:
                    self.counter += 1
                mask = mask<<1	
    	return self.counter
    
    def estimate(self):
        c = float(min(M - 1, self.count_zero_bits()))
    	size = math.log(c/M) / (K * math.log(1.0-1.0/M))
        return size
    
    def extend(self, other):
        self.bloom = ''.join(chr(ord(i) | ord(j)) for i,j in zip(self.bloom, other.bloom))
        return self.bloom
    


    
    
    
    
