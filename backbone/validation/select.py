import cjson
from collections import defaultdict,deque
from operator import itemgetter
import sys
from copy import deepcopy
from math import log
from random import randint,shuffle
import sys
import itertools
infile='../user_tag_dict_sf1'
outfile='./user_tag_dict_sf_selected'

def select_high_user(infile,outfile):
	outfile=open(outfile,'w')
	for line in open(infile):
		line1=cjson.decode(line)
		if len(line1[1])>50:
			outfile.write(line)


def data_prepration(nfold,data_file):#user_tag_dict_1
    outfile=[]
    #tagdict=[]
    for i in range(nfold):
        outfile.append(open(data_file+'_part'+str(i+1),'w'))
        
    for line in open(data_file,'r'):
        tagdict=[{} for i in range(nfold)]
        #print tagdict
        line=cjson.decode(line)
        n=len(line[1])/nfold
        fn=n*nfold
        itera=0
        randlist=[i for i in range(len(line[1]))]
        shuffle(randlist)
        taglist=[]
        for key,value in line[1].iteritems():
            taglist.append([key,value])
        for inx in randlist:
            num=0
            if num<fn:
                index=itera%nfold
                key=taglist[inx][0]
                value=taglist[inx][1]
                if index>0:
                	index=1
                tagdict[index][key]=value
                itera+=1
            else:
                index=randint(0,nfold-1)
                tagdict[index][key]=value
        for i in range(nfold):
            outfile[i].write(cjson.encode([line[0],tagdict[i]])+'\n')


if __name__ == '__main__':
	select_high_user(infile,outfile)
	data_prepration(4,outfile)