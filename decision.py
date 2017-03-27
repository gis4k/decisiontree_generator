from __future__ import division
import numpy as np
import scipy as sp
import scipy.stats


#xx = np.loadtxt("homework3data(temp365).txt", dtype='float', comments='#', delimiter=None, converters=None, skiprows=0, usecols=None, unpack=False, ndmin=0)
#xx = np.loadtxt("mush.data", dtype='unicode', comments='#', delimiter=None, converters=None, skiprows=0, usecols=None, unpack=False, ndmin=0)
#xx = np.loadtxt("mush.data",dtype='int',comments='#', delimiter=',')
xx =np.recfromcsv("mush.data", delimiter=',', filling_values=np.nan, case_sensitive=True, deletechars='', replace_space=' ')


#sp.stats.entropy(x[], qk=None, base=None)[source]

print(xx)

print("hi")
print(xx[0][0])
print(xx[1][0])

print(type(xx))

print(np.shape(xx))


#this is 0.940
e = [9/14, 5/14]
print(sp.stats.entropy(e,base =2))

'''
read .names file.
'''
nm = open('mush.names', 'r')
#remove crlf of windows.
print(nm)
nmt = nm.read().replace('\r\n','').replace(',','').split('.')


#print(len(nmt.pop(0)))
decision = set(nmt.pop(0).translate(None, ','))
nmt.pop(-1)

print(decision)
print(len(decision))

arg_list = list()
name_dict = dict()
for x in nmt:
	nd =x.split(':')
	print(nd)
	name_dict[nd[0]] = set(nd[1])
	arg_list.append(nd[0])

print(name_dict)
print(name_dict[arg_list[0]])