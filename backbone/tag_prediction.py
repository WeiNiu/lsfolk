#from __future__ import division
import cjson
from collections import defaultdict,deque
from operator import itemgetter
import sys
from copy import deepcopy
from math import log
from random import randint,shuffle
import sys
import itertools

earthRadiusMiles = 3958.761
def getHaversineDistance(origin, destination, radius=earthRadiusMiles):
    lat1, lon1 = origin
    lat2, lon2 = destination
              #radius = 6371 # km
    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
             * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c
    return d

name=['chicago','new_york','la','sf','houston','miami','atlanta','indiana','seatle','dallas']
target_loc=[[41.84,-87.68],[40.71,-73],[34.05,-118.24],[37.77,-122.42],[29.76,-95.36],[25.76,-80.19],[33.74,-84.38],[39.95,-75.16],[47.6,-122.3],[32.77,-96.8]]

class TagPrediction(object):
    def data_prepration(self,nfold,data_file):#user_tag_dict_1
        outfile=[]
        #tagdict=[]
        for i in range(nfold):
            outfile.append(open('./validation/'+data_file+'_fold'+str(i+1),'w'))
            
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
                    tagdict[index][key]=value
                    itera+=1
                else:
                    index=randint(0,nfold-1)
                    tagdict[index][key]=value
            for i in range(nfold):
                outfile[i].write(cjson.encode([line[0],tagdict[i]])+'\n')
                
    def construct_training(self,infiles,xfold):
        files=[]
        infile=infiles[0].split('_fold')[0]
        print infile
        outfile=open('./validation/'+infile+'_train_'+str(xfold),'w')
        for filename in infiles:
            files.append(open('./validation/'+filename,'r'))
        
        while True:
            tagdict={}
            tag=''
            for i in files:
                x=i.readline()
                if x=="":
                    return False
                else:
                    [tag,tagd]=cjson.decode(x)
                #print tag,tagd

                tagdict.update(tagd)
            outfile.write(cjson.encode([tag,tagdict])+'\n')
    def nfold_(self,nfold,docs) :
        combs=list(itertools.combinations(docs,nfold-1))
        for comb in combs:
            for filename in docs:
                if filename not in comb:
                    xfold=filename.split('fold')[-1]
            self.construct_training(comb,xfold)
    
if __name__ =='__main__':
    data=TagPrediction()
    data.data_prepration(4,'user_tag_dict_lchou1')
    #data.data_prepration(4,sys.argv[1])
    docs=['user_tag_dict_lchou1_fold1','user_tag_dict_lchou1_fold2','user_tag_dict_lchou1_fold3','user_tag_dict_lchou1_fold4']
    #data.construct_training(['user_tag_dict_houston1_fold1','user_tag_dict_houston1_fold2','user_tag_dict_houston1_fold3'],4)
    data.nfold_(4,docs)
