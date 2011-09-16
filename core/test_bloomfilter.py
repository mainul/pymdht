# Copyright (C) 2011 Md. Mainul Hossain
# Released under GNU LGPL 2.1
# See LICENSE.txt for more information


#import message
#import node
#import ptime

from nose.tools import ok_, eq_
import bloomfilter

bf = bloomfilter.BloomFilter()

list_ip = ['192.0.2.%d' %(i) for i  in range(256)]
list_ip6 = ['2001:DB8::%X' %(i) for i  in range(0x0, 0x3E8)]

for ip in list_ip:
	bf.insert_ip(ip)


for ip in list_ip6:
    bf.insert_ip(ip)



print bf.hex_repr()
print bf.estimate()

