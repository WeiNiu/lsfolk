from __future__ import division
import cjson
from collections import defaultdict,deque
from operator import itemgetter
import sys
from copy import deepcopy
from math import log
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

name=['chi','ny','la','sf','hou','miami','london','sydney','seattle','dallas']
target_loc=[[41.84,-87.68],[40.71,-73],[34.05,-118.24],[37.77,-122.42],[29.76,-95.36],[25.76,-80.19],[33.74,-84.38],[39.95,-75.16],[47.6,-122.3],[32.77,-96.8]]

class Locallist(object):
    #identify local tag by the percentage difference
    def local_percentage(self,locs):
        loc_tag_dict=defaultdict(dict)
        taglist=[]
        for item in locs:
            filename='./tag_freq_dict_'+item
            readfile=open(filename,'r')
            total_cnt=0
            itemdict= cjson.decode(readfile.readline())
            for key,value in itemdict.iteritems():
                total_cnt+=value
            for key in itemdict:
                itemdict[key]=value/total_cnt
                if value/total_cnt>0.00001:
                    taglist.append(key)
                #use median
                loc_tag_dict[item]=itemdict
        taglist=set(taglist)
        citycompare=defaultdict(dict)
        for tag in taglist:
            
            for key in loc_tag_dict:
                citycompare[tag][key]=loc_tag_dict[key].get(tag,0)
            #print tag,citycompare[tag]
            rank=sorted(citycompare[tag].items(),key=itemgetter(1))
            median=rank[4]+rank[5]
        
        return citycompare
    #identify local tag by the tag percentage entropy over the locations
    def tag_percentage_entropy(self,citycompare):
        out=open('./entropy1','w')
        entropydict={}
        for tag in citycompare:
            print tag
            sum1=0
            for key,value in citycompare[tag].iteritems():
                sum1+=value
            entropy=0
            for key,value in citycompare[tag].iteritems():
                #print sum1,value
                if value!=0:
                    entropy+=(-(value/sum1)*log(value/sum1,2))
            entropydict[tag]=entropy
        e=sorted(entropydict.items(),key=itemgetter(1))
        #for item in e:
        out.write(cjson.encode(e))
    #show that different tag pair tend to bond differently
    def construct_pair(self,list1,list2):
        tagp=[]
        for item in list1:
            for sup in list2:
                tagp.append([item,sup])
        return tagp
    def check_rulelist(self,pairs):
        relation=defaultdict(dict)
        for loc in name:
            infile=open('./rulelist_'+loc,'r')
            for line in infile:
                #print line,loc
                line=cjson.decode(line) 
                #if loc=='dallas' and line[0]=='maverick'and line[1]=='nba':
                #    print line
                alias={"dalla maverick":"maverick"}
                if line[0] in alias:
                    line[0]=alias[line[0]]
                if [line[0],line[1]] in pairs: 
                    relation[line[0]+'_'+line[1]][loc]=[line[2],'p']
                elif [line[1],line[0]] in pairs:
                    relation[line[0]+'_'+line[1]][loc]=[line[2],'n']
        return relation

    def tag_pair_distance_at_different_location(self,outfile):
        outfile=open(outfile,'w')
        tagpair1=[['rocket','laker','maverick','warrior','bull','basketball'],['oil','green'],['business','stock','investment'],['olympic','rugby'],['comedy','haha'],['dev'],['museum']]
        tagpair2=[['nba'],['energy'],['finance'],['sport'],['funny'],['coding'],['art']]
        pairs = self.construct_pair(tagpair1[1],tagpair2[1])
        print pairs
        vvs=self.check_rulelist(pairs)
        for key,value in vvs.iteritems():
            outfile.write(cjson.encode(key))
            outfile.write(cjson.encode(value)+'\n')
        return vvs

if __name__=='__main__':
    l=Locallist()
    #citycompare=l.local_percentage(name)
    #l.tag_percentage_entropy(citycompare)

    l.tag_pair_distance_at_different_location('tagpair_eg1')
