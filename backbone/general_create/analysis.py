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

name=['chicago','new_york','la','sf','houston','miami','atlanta','indiana','seatle','dallas']
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
    def tag_pair_distance_at_different_location():
        pass

if __name__=='__main__':
    l=Locallist()
    citycompare=l.local_percentage(name)
    l.tag_percentage_entropy(citycompare)
