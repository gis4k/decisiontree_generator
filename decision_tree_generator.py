from __future__ import division
from collections import OrderedDict
import numpy as np
from io import BytesIO
import scipy as sp
import scipy.stats
import copy
import sys

#names and data.
#after cpy. del dct[key]
#dct.keys().index('keyval')
#name_dict structure : OrderedDict( [ ('result', ['p', 'e']), ('cap-shape', ['c', 'b', 'f', 'k', 's', 'x']),,,,,])
name_dict=OrderedDict()
dat='nan'
tet = 'nan'

class Dtree_node(object):

    def __init__(self, edge_name, part_data, last_arg, par_name):
        global name_dict

        self.arg_name = 'not_decided'
        self.par_name = par_name

        self.edge_name = edge_name
        self.part_data = part_data

        self.part_len = len(self.part_data)

        #deep copy usued argument list.
        self.last_arg = copy.deepcopy(last_arg)

        #initialize tot_ent
        if self.part_len != 0:
            self.tot_ent =self.ent_calc(self.part_data)
        else:
            self.tot_ent = 0

        self.children = []
        self.decision = 'nan'
        self.flag = ''

        #terminal decision.

        #if there's no data. then default eatable. and set terminal.
        if (self.part_len == 0) :
            self.flag='tml'
            #name_dict[name_dict.keys()[0]][0] is first item of result. ex) in mush 'e'
            self.decision = name_dict[name_dict.keys()[0]][0]

        #if given data's entropy is 0. then decision by counting.
        elif self.tot_ent==0 | (len(self.last_arg) == len(name_dict)) :
            self.flag='tml'
            s,e,p = self.counter(part_data)

            if e>=p:
                self.decision = name_dict[name_dict.keys()[0]][0]
            else :
                self.decision = name_dict[name_dict.keys()[0]][1]

        #print(self.tot_ent)
        print('son of '+self.par_name+' from edge : '+self.edge_name+ ' dat len : ('+str(self.part_len)+ ') tot_ent : '+ str(self.tot_ent) + ' result : ' +str(self.counter(self.part_data)) +' decision : ' +self.decision)

    #by calculating Entropy gain, decide self argument.
    def form_tree(self):

        #skip first result row.
        iterarg =iter(name_dict.keys())
        next(iterarg)
        
        gainDct=OrderedDict()

        for x in iterarg:

            el = list()
            for y in name_dict[x]: 
                
                if x not in self.last_arg:
                    #make table Dv for Ent(Dv).
                    t, l = self.select(x,y, self.part_data)

                    #calc (Dv/D) * Ent(Dv).
                    el.append( (l/self.part_len) * self.ent_calc(t) )
                else:
                    #if it was used arg by parents, then make infi high ent vaule.
                    el.append(999)

            #sigma (Dv/D) * Ent(Dv) values to k.
            k=0
            for z in el:
                k+=z
            #Gain(D,A).
            gainDct[x]=self.tot_ent-k

        #Find max Gain.
        mx = max(gainDct.values())
        idx =0
        for i,z in enumerate(gainDct):
            if gainDct[z] == mx:
                idx = i
                self.arg_name=z

        #mark used argument.
        self.last_arg.append(self.arg_name)

        print('**im edgefrom : '+self.edge_name + ' found that i am : '+self.arg_name + ' Ent was ' +str(self.tot_ent) + ' my max :'+str(mx))
            

    def add_child(self):

        if self.flag != 'tml':
            print('--im edgefrom : '+self.edge_name+ ' making child because iam :'+self.arg_name+ ' not terminal and father is :' + self.par_name)
            print('--im arg: "'+self.arg_name +'" my child edges ' + str(name_dict[self.arg_name]))

            egn = name_dict[self.arg_name]
            #print(egn)

            for x in egn:
                self.children.append( Dtree_node(x, self.select(self.arg_name, x, self.part_data)[0], self.last_arg , self.arg_name) )

        return self.children


    #return rows by arg_name & edge_name.
    def select(self, selct_arg_name, selct_edge_name, target_dat):

        i = name_dict.keys().index(selct_arg_name)

        neodat = list()
        for x in target_dat:
            if x[i] == selct_edge_name:
                neodat.append(x)
        
        neodat = np.array(neodat)

        return neodat, len(neodat)


    #calculate entropy of rows by count indat[0] result.
    def ent_calc(self, indat):

        s,e,p=self.counter(indat)

        if s!=0:
            ent_ary = list()
            ent_ary.append(e/s)
            ent_ary.append(p/s)
            #print(ent_ary)

            return sp.stats.entropy(ent_ary,base =2)
        elif s==0:
            return 0

    #return sum, positive, negative counting.
    def counter(self,indat):
        s=e=p=0
        for x in indat:
            if name_dict[name_dict.keys()[0]][0] == x[0] :
                e+=1
            s+=1
        p = s-e

        return s,e,p


#this is 0.940. entropy calculating.
#e = [9/14, 5/14]
#print(sp.stats.entropy(e,base =2))

#read names, data file. set global name_dict & dat.
def name_data_reader(namefile, datafile):

    global name_dict
    nm = open(namefile, 'r')

    #remove crlf of windows.
    nmt = nm.read().replace('\r\n','').replace(',','').split('.')
    nmt.pop(-1)

    for x in nmt:
        nd =x.split(':')
        name_dict[nd[0]] = list(nd[1])

    global dat
    dat = np.genfromtxt(datafile, delimiter=',',dtype=str)


#traverse node and test, return 1 if right.
def tester(h,dat):
    dat = list(dat)
    res = dat.pop(0)

    for x in dat:
        if h.flag != 'tml':
            for c in h.children:
                #minus one index because result was poped.
                if c.edge_name==dat[name_dict.keys().index(h.arg_name) -1]:
                    print('my_arg :' + h.arg_name + ' selected edge : '+ c.edge_name)
                    h=c
                    break

        elif h.flag =='tml':
            print('decision : ' +h.decision)
            if res == h.decision:
                return 1
            else:
                return 0

def main():
    #Usage
    if len(sys.argv) != 4 :
        print('Usage : python script <.names> <.data> <.test>')
        sys.exit()

    #read file.
    name_data_reader(sys.argv[1],sys.argv[2])
    
    #Head node.
    h = Dtree_node('root', dat, list(),'rooot')
    h.form_tree()

    #level order forming as much len(argument)-1 - except result
    clist = h.add_child()
    i=0
    while i < len(name_dict)-1:
        tmp = list()
        for x in clist:
            if x.flag != 'tml':
                x.form_tree()
                tmp += x.add_child()

        clist = list()
        clist = tmp

        i+=1

    #test accuracy.

    tet = np.genfromtxt(sys.argv[3], delimiter=',',dtype=str)  

    r=0
    for i,x in enumerate(tet):
        print('Case #'+str(i+1))
        r += tester(h,x)

    print('\nlearning data : ' +str(len(dat)))
    print('total test case : '+str(len(tet))+ ' right answers : '+ str(r) + ' wrong  answers: '+ str(len(tet)-r))
    print('test accuracy is ' + str( (r/len(tet))*100))


if __name__ == "__main__":
    main()
