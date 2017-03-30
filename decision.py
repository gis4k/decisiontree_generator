from __future__ import division
from collections import OrderedDict
import numpy as np
import scipy as sp
import scipy.stats

#names and data.
#after cpy del dct[key]
name_dict=OrderedDict()
dat='nan'

class Dtree_node(object):
    def __init__(self, data):
        self.data = data
        self.children = []

    def add_child(self, obj):
        self.children.append(obj)

    def form_tree():
        pass

    def ent_calc():
        pass


#this is 0.940. entropy calculating.
e = [9/14, 5/14]
print(sp.stats.entropy(e,base =2))

#read names, data file. set name_dict & dat.
def name_data_reader(namefile, datafile):

    global name_dict
    nm = open(namefile, 'r')
    #remove crlf of windows.
    print(nm)
    nmt = nm.read().replace('\r\n','').replace(',','').split('.')
    nmt.pop(-1)
    #name_dict = dict()

    #global name_dict
    #arg_list = list()
    for x in nmt:
        nd =x.split(':')
        #remove duplication by using set.
        name_dict[nd[0]] = list(set(nd[1]))
        #arg_list.append(nd[0])

    #print(name_dict.items()[0][1][0])
    '''dict for names'''
    print(name_dict)

    global dat
    dat =np.recfromcsv(datafile, delimiter=',', filling_values=np.nan, case_sensitive=True, deletechars='', replace_space=' ')









def main():
    name_data_reader('mush.names','mush.data')



if __name__ == "__main__":
    main()