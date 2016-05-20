from __future__ import division
from collections import defaultdict
from datetime import datetime
#from library.geo import UTMConverter
import cjson
import time
from math import fabs,log10,exp,log
from operator import itemgetter
from library.mrjobwrapper import ModifiedMRJob
from library.twitter import getDateTimeObjectFromTweetTimestamp
from library.geo import getHaversineDistance
from copy import deepcopy
import re,math
#from nltk import PorterStemmer
#from nltk.corpus import stopwords
earthRadiusMiles = 3958.761
earthRadiusKMs = 6371.009
earthCircumferenceInMiles = 24901.55
ACCURACY = 10 ** 2 # UTM boxes in meter
ACCURACIES = [10 ** 3, 10 ** 4, 10 ** 5]
START_TIME, END_TIME = datetime(2011, 2, 1), datetime(2013, 3, 31)

# Parameters for the MR Job that will be logged.
HASHTAG_STARTING_WINDOW = time.mktime(START_TIME.timetuple())
HASHTAG_ENDING_WINDOW = time.mktime(END_TIME.timetuple())


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

def merge_dict(dicts):
    combine_dict=defaultdict(int)
    for d in dicts:
        for key,value in d.iteritems():
            combine_dict[key]=combine_dict.get(key,0)+d[key]
    return combine_dict

def get_HD_from_UTMLL(u1,u2, radius=earthRadiusKMs):
    lat1,long1,_=u1.split('_')
    corr1=(float(lat1),float(long1))
    lat2,long2,_=u2.split('_')
    corr2=(float(lat2),float(long2))
    dist=getHaversineDistance(corr1,corr2,radius)
    return dist

def iterate_reduced_tweets(line):
    data = cjson.decode(line)
    loc = None
    if 'geo' in data: loc = data['geo']
    else: loc = data['bb']
    if data['id'] != None: uid = data['id']
    time1 = time.mktime(getDateTimeObjectFromTweetTimestamp(data['t']).timetuple())# make time represent as sec from 9 tuple
#this here is selecting place in US.
#    if loc[0]>24.52 and loc[0]<49.38 and loc[1]<-66.95 and loc[1]>-124.77:
#    if loc[0]>40.48 and loc[0]<40.90 and loc[1]<-73.69 and loc[1]>-74.25:
#    if loc[0]>40.7022 and loc[0]<40.807 and loc[1]<-73.927 and loc[1]>-74.0218:
    for h in data['h']: yield h.lower(), (loc, time1, uid)

'''
this function will tokenize, steming, (and remove the common noise).
'''
class ReadFile:
    @staticmethod
    def read_json_yield_uid(line):
        line = cjson.decode(line)
        user_id=line['user_id']
        tags=line['tag']
        for tag in set(tags):
            yield user_id,tag

    @staticmethod
    def read_json_yield_tagger(line):
        line = cjson.decode(line)
        list_creator_id=line['list_creator_id']
        tags=line['tag']
        for tag in set(tags):
            line1=deepcopy(line)
            line1['tag']=[tag]
            yield tag,[list_creator_id,line1]

    @staticmethod
    def read_json_yield_tag(line):
        line = cjson.decode(line)
        user_id=line['user_id']
        tags=line['tag']
        for tag in set(tags):
            line1=deepcopy(line)
            line1['tag']=[tag]
            yield tag,line1
    @staticmethod
    def read_json_yield_user(line):
        line=cjson.decode(line)
        user_id=line['user_id']
        list_creator_id=line['list_creator_id']
        list_creator_lat=line['list_creator_lat']
        list_creator_lng=line['list_creator_lng']
        user_lat=line['user_lat']
        user_lng=line['user_lng']
        yield user_id,[list_creator_id,list_creator_lat,list_creator_lng,user_lat,user_lng]
    @staticmethod
    def read_json_yield_ll(line):
        line=cjson.decode(line)
        user_id=line['user_id']
        list_id=line['list_id']
        tags=line['tag']
        cr_id=line['list_creator_id']
        #list_creator_lat=line['list_creator_lat']
        #list_creator_lng=line['list_creator_lng']
        #user_lat=line['user_lat']
        #user_lng=line['user_lng']
        for tag in set(tags):
            yield user_id,[tag,list_id]
           #yield cr_id,[tag,list_id]
    @staticmethod
    def read_json_yield_list(line):
        line=cjson.decode(line)
        user_id=line['user_id']
        list_id=line['list_id']
        tags=line['tag']
        cr_id=line['list_creator_id']
        #list_creator_lat=line['list_creator_lat']
        #list_creator_lng=line['list_creator_lng']
        #user_lat=line['user_lat']
        #user_lng=line['user_lng']
        #for tag in set(tags):
        #yield user_id,list_id
        yield list_id,[cr_id,user_id]
        #yield cr_id,list_id
######################################
# No corpus.stopword exist on server #
# Try single thread version on rex   #
######################################

class SiftTag(ModifiedMRJob):
    DEFAULT_INPUT_PROTOCOL = 'raw_value'
    def __init__(self,
                 *args,
                 **kwargs):
        super(SiftTag,self).__init__(*args,**kwargs)
    def map_line_to_tag(self,key,line):
        if False:yield
        #user_tag_dict={}
        #Preprocessing
        for tag,line in ReadFile.read_json_yield_tag(line):
            yield tag,line
    def red_tag_to_dict(self,tag,lines):
        #user_tag_dict={}
        #for tag in tags:
        #    user_tag_dict[tag]=user_tag_dict.get(tag,0)+1
        lines=list(lines)
        if len(lines)>=5:
            for line in lines:
                yield tag,line
        else: pass
    def steps(self):
        return[self.mr(
                mapper=self.map_line_to_tag,\
                reducer=self.red_tag_to_dict
        )]
class SiftTagByTagger(ModifiedMRJob):
    DEFAULT_INPUT_PROTOCOL = 'raw_value'
    def __init__(self,
                 *args,
                 **kwargs):
        super(SiftTagByTagger,self).__init__(*args,**kwargs)
    def map_line_to_tag(self,key,line):
        if False:yield
        #user_tag_dict={}
        #Preprocessing
        for tag,line in ReadFile.read_json_yield_tagger(line):
            yield tag,line
    def red_tag_to_dict(self,tag,lines):
        #user_tag_dict={}
        #for tag in tags:
        #    user_tag_dict[tag]=user_tag_dict.get(tag,0)+1
        lines=list(lines)
        uid_list=[a[0] for a in lines]
        #uid_list=list(uids)
        uid_set=set(uid_list)
        if len(uid_set)>=3:
            for line in lines:
            #    line['tag']=tag
                yield tag,line[1]
        else: pass

    def steps(self):
        return[self.mr(
                mapper=self.map_line_to_tag,\
                reducer=self.red_tag_to_dict
        )]
#
#each tag occurrence, one line from each list name, one line
class UserTagDict(ModifiedMRJob):
    DEFAULT_INPUT_PROTOCOL = 'raw_value'
    def __init__(self,
                 *args,
                 **kwargs):
        super(UserTagDict,self).__init__(*args,**kwargs)
    def map_line_to_user_tag(self,key,line):
        if False:yield
        #user_tag_dict={}
        #Preprocessing
        for user_id,tag in ReadFile.read_json_yield_uid(line):
            yield user_id,tag
    def red_user_tag_to_dict(self,user_id,tags):
        user_tag_dict={}
        for tag in tags:
            user_tag_dict[tag]=user_tag_dict.get(tag,0)+1
        yield user_id,[user_id,user_tag_dict]
    def steps(self):
        return[self.mr(
                mapper=self.map_line_to_user_tag,\
                reducer=self.red_user_tag_to_dict
        )]

class ZJ_inlist(ModifiedMRJob):
    DEFAULT_INPUT_PROTOCOL = 'raw_value'
    def __init__(self,
                 *args,
                 **kwargs):
        super(ZJ_inlist,self).__init__(*args,**kwargs)
        user_inlist={}
    def map_line_to_user_tag(self,key,line):
        if False:yield
        #user_tag_dict={}
        #Preprocessing
        for user_id,[tag,listid] in ReadFile.read_json_yield_ll(line):
            yield user_id,[tag,listid]
    def red_user_tag_to_dict(self,user_id,info):
        user_inlist=defaultdict(list)
        for inf in info:
            user_inlist[inf[0]].append(inf[1])
        for key,value in user_inlist.iteritems():
            user_inlist[key]=list(set(value))
        yield user_id,[user_id,user_inlist]
    def steps(self):
        return[self.mr(
                mapper=self.map_line_to_user_tag,\
                reducer=self.red_user_tag_to_dict
        )]
class ZJ_list(ModifiedMRJob):
    DEFAULT_INPUT_PROTOCOL = 'raw_value'
    def __init__(self,
                 *args,
                 **kwargs):
        super(ZJ_list,self).__init__(*args,**kwargs)
        user_inlist={}
    def map_line_to_user_tag(self,key,line):
        if False:yield
        #user_tag_dict={}
        #Preprocessing
        for listid,[cr,user] in ReadFile.read_json_yield_list(line):
            yield listid,[cr,user]
    def red_user_tag_to_dict(self,list_id,info):
        list_dict={}
        list_dict['users_in_list']=[]
        for [cr,user] in info:
            list_dict['list_creator_id']=cr
            list_dict['users_in_list'].append(user)
        list_dict['users_in_list']=list(set(list_dict['users_in_list']))
        list_dict['list_id']=list_id
        yield list_id,list_dict
    def steps(self):
        return[self.mr(
                mapper=self.map_line_to_user_tag,\
                reducer=self.red_user_tag_to_dict
        )]


class TagCooccur(ModifiedMRJob):
    DEFAULT_INPUT_PROTOCOL = 'raw_value'
    def __init__(self,
                 *args,
                 **kwargs):
        super(TagCooccur,self).__init__(*args,**kwargs)
    def map_line_to_user_tag(self,key,line):
        if False:yield
        line=cjson.decode(line)
        for key,value in line[1].iteritems():
            for key1,value1 in line[1].iteritems():
                if key!=key1:
                    t=[key,key1]
                    t1=sorted(t)
                    yield str(t1[0])+'_'+str(t1[1]),1
                    #yield str(t1[0])+'_'+str(t1[1]),min(value,value1)
                else:continue
    def red_user_tag_to_dict(self,tag,value):
        yield tag,[tag,sum(value)] 
    def steps(self):
        return[self.mr(
                mapper=self.map_line_to_user_tag,\
                reducer=self.red_user_tag_to_dict
        )]
# difference is this use minimum occurance time.
class TagCooccur1(ModifiedMRJob):
    DEFAULT_INPUT_PROTOCOL = 'raw_value'
    def __init__(self,
                 *args,
                 **kwargs):
        super(TagCooccur1,self).__init__(*args,**kwargs)
        self.tagdict={}
    def map_line_to_user_tag(self,key,line):
        if False:yield
        line=cjson.decode(line)
        for key,value in line[1].iteritems():
            for key1,value1 in line[1].iteritems():
                if key!=key1:
                    t=[key,key1]
                    t1=sorted(t)
                    self.tagdict[str(t1[0])+'_'+str(t1[1])]=self.tagdict.get(str(t1[0])+'_'+str(t1[1]),0)+1
                    #yield str(t1[0])+str(t1[1]),min(value,value1)
                else:continue

    def map_final_line_to_user_tag(self):
        yield 'abc',self.tagdict
    def red_user_tag_to_dict(self,key,dicts):
        combineddict=merge_dict(dicts)
        yield key,combineddict
    def steps(self):
        return[self.mr(
                mapper=self.map_line_to_user_tag,\
                mapper_final=self.map_final_line_to_user_tag,\
                reducer=self.red_user_tag_to_dict
        )]

class TopicRank(ModifiedMRJob):
    DEFAULT_INPUT_PROTOCOL = 'raw_value'
    def __init__(self,
                 *args,
                 **kwargs):
        super(TopicRank,self).__init__(*args,**kwargs)
    def map_line_to_user_tag(self,key,line):
        if False:yield
        #user_tag_dict={}
        #Preprocessing
        for uid,tag in ReadFile.read_json_yield_uid(line):
            yield tag,1
    def red_user_tag_to_dict(self,tag,value):
        #tag_freq_dict={}
        yield tag,[tag,sum(value)] 
    def steps(self):
        return[self.mr(
                mapper=self.map_line_to_user_tag,\
                reducer=self.red_user_tag_to_dict
        )]

class GetWordFreq(ModifiedMRJob):
    DEFAULT_INPUT_PROTOCOL = 'raw_value'    
    def __init__(self,
                 *args,
                 **kwargs):
        super(GetWordFreq, self).__init__(*args, **kwargs)
        self.tagcount=0
        self.tweetcount=0
        self.tweetwithtagcount=0
    def map_line_to_count(self,key,line):
        if False:yield
        for hashtag, (location, occ_time, uid) in iterateReducedTweets(line):
            self.tagcount+=1
        if pre < self.tagcount:
            self.tweetwithtagcount+=1
        self.tweetcount+=1
    def map_final_line_to_count(self):
        yield 'abc', (self.tagcount,self.tweetcount,self.tweetwithtagcount)
    def red_count_to_count(self,key,value):
        tagcount=0
        tweetcount=0
        tweetwithtagcount=0
        for item in value:
            tagcount+=item[0]
            tweetcount+=item[1]
            tweetwithtagcount+=item[2]
        yield 'abc',(tagcount,tweetcount,tweetwithtagcount)
    def steps(self):
        return [self.mr(mapper=self.map_line_to_count,\
                        mapper_final=self.map_final_line_to_count,\
                        reducer=self.red_count_to_count)]
    

class SP(ModifiedMRJob):
    DEFAULT_INPUT_PROTOCOL = 'raw_value'
    def __init__(self,
                 *args,
                 **kwargs):
        super(SP, self).__init__(*args, **kwargs)
        self.hou=[29.76,-95.37]
        self.sf=[37.77, -122.42]
        self.ny=[40.71,-74.00]
        self.chi=[41.89,-87.63]
        self.q=self.hou
        self.query_lat=self.q[0]
        self.query_lng=self.q[1]
        self.dmin=100
        self.alpha=1.01
    def map_line_to_user(self,key,line):
        if False:yield
        for user,creator in ReadFile.read_json_yield_user(line):
            dist=getHaversineDistance([creator[1],creator[2]],[self.query_lat,self.query_lng])
            s=(self.dmin/(dist+self.dmin))**1.01
            yield user,[s,creator[3],creator[4]]

    def red_user_to_score(self,user,value):
        sumv = 0
        cnt=0
        for v in value:
            sumv += v[0]
            cnt+=1
        yield user,(user, sumv/cnt,v[1],v[2])

    def steps(self):
        return[self.mr(mapper=self.map_line_to_user,\
                       reducer=self.red_user_to_score)]
'''Count the number of times each person has been labeled, modified for cognos. add distance weight
'''
class CountLabel(ModifiedMRJob):
    DEFAULT_INPUT_PROTOCOL = 'raw_value'
    def __init__(self,
                 *args,
                 **kwargs):
        super(CountLabel, self).__init__(*args, **kwargs)
        self.hou=[29.76,-95.37]
        self.sf=[37.77, -122.42]
        self.ny=[40.71,-74.00]
        self.chi=[41.89,-87.63]
        self.q=self.chi
        self.query_lat=self.q[0]
        self.query_lng=self.q[1]

        self.dmin=100
        self.alpha=1.01

    def map_line_to_user(self,key,line):
        if False:yield
        for user,creator in ReadFile.read_json_yield_user(line):
            dist=getHaversineDistance([creator[1],creator[2]],[self.query_lat,self.query_lng])
            s=(self.dmin/(dist+self.dmin))**1.01
            yield user,[s,creator[3],creator[4]]

    def red_user_to_score(self,user,value):
        sumv = 0
        cnt=0
        for v in value:
            sumv += v[0]
            cnt+=1
        yield user,(user, sumv, v[1], v[2])


    def steps(self):
        return[self.mr(mapper=self.map_line_to_user,\
                       reducer=self.red_user_to_score)]


if __name__ == '__main__':
    #Preprocessing.run()
    #UserTagDict.run()
    #TopicRank.run()
    #TagCooccur.run()
    #TagCooccur1.run()
    SiftTag.run()
    #SP.run()
    #ZJ_list.run()
    #ZJ_inlist.run()
    #CountLabel.run()
    #SiftTagByTagger.run()
