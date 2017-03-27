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

a = ['n','n','y','y','y','n','y','n','y','y','y','y','y','n']

b = [0,0,1,1,1,0,1,0,1,1,1,1,1,0]
c = [1,1,1,1,1,1,1,1,1,1,1,1,1,1]

d = [1,1,1,1,1,1,1,0,0,0,0,0,0,0]



print(sp.stats.entropy(b,c,2))
print(sp.stats.entropy(d,c,2))


#this is 0.940
e = [9/14, 5/14]
print(sp.stats.entropy(e,base =2))
