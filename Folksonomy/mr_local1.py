from __future__ import division
from collections import defaultdict
from datetime import datetime
#from library.geo import UTMConverter
import cjson
import time
from math import fabs,log10,exp,log
from operator import itemgetter
from mrjob.job import MRJob
from library.twitter import getDateTimeObjectFromTweetTimestamp
from library.geo import getHaversineDistance
from copy import deepcopy
import re,math
earthRadiusMiles = 3958.761
earthRadiusKMs = 6371.009
earthCircumferenceInMiles = 24901.55
ACCURACY = 10 ** 2 # UTM boxes in meter
ACCURACIES = [10 ** 3, 10 ** 4, 10 ** 5]
START_TIME, END_TIME = datetime(2011, 2, 1), datetime(2013, 3, 31)
target_loc=[41.84,-87.68]#chi
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
    def read_json_yield_uid1(line):
        line = cjson.decode(line)
        user_id=line['user_id']
        tags=line['tag']
        lat1=line['list_creator_lat']
        lng1=line['list_creator_lng']
        user_lat=line['user_lat']
        user_lng=line['user_lng']
        distance=getHaversineDistance([lat1,lng1],[user_lat,user_lng])
        for tag in set(tags):
            yield user_id,[tag,distance]
    @staticmethod
    def read_json_yield_uid2(line):
        line = cjson.decode(line)
        user_id=line['user_id']
        tags=line['tag']
        lat1=line['list_creator_lat']
        lng1=line['list_creator_lng']
        user_lat=line['user_lat']
        user_lng=line['user_lng']
        distance=getHaversineDistance(target_loc,[user_lat,user_lng])
        if distance <= 10:
            distance=0
        elif distance > 10:
            distance-=10
        for tag in set(tags):
            yield user_id,[tag,distance]

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
    @staticmethod
    def read_utd_yield_tag_pair(line):
        line=line.split('\t')[1]
        line=cjson.decode(line)[1]
        for key,value in line.iteritems():
            for key1,value1 in line.iteritems():
                yield key+'_'+key1,min(value,value1)
                
#
class SiftTag(MRJob):
    #DEFAULT_INPUT_PROTOCOL = 'raw_value'
    #def __init__(self,
    #             *args,
    #             **kwargs):
    #    super(SiftTag,self).__init__(*args,**kwargs)
    def map_line_to_tag(self,key,line):
        if False:yield
        #user_tag_dict={}
        #Preprocessing
        for tag,line in ReadFile.read_json_yield_tag(line):
            #if re.search(' ',tag):
            yield tag,line
    def red_tag_to_dict(self,tag,lines):
        #user_tag_dict={}
        #for tag in tags:
        #    user_tag_dict[tag]=user_tag_dict.get(tag,0)+1
        lines=list(lines)
        #lines=set(lines)
        if len(lines)>=10:
            for line in lines:
                yield tag,line
        else: pass
    def steps(self):
        return[self.mr(
                mapper=self.map_line_to_tag,\
                reducer=self.red_tag_to_dict
        )]
class SiftTagByTagger(MRJob):
    DEFAULT_INPUT_PROTOCOL = 'raw_value'
    def __init__(self,
                 *args,
                 **kwargs):
        super(SiftTagByTagger,self).__init__(*args,**kwargs)
    def map_line_to_tag(self,key,line):
        if False:yield
        #user_tag_dict={}
        #Preprocessing
        line=line.split('\t')[1]
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
        if len(uid_set)>=5:
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
class UserTagDict(MRJob):
    #DEFAULT_INPUT_PROTOCOL = 'raw_value'
    #def __init__(self,
    #             *args,
    #             **kwargs):
    #    super(UserTagDict,self).__init__(*args,**kwargs)
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
class TagUserDict(MRJob):
    #DEFAULT_INPUT_PROTOCOL = 'raw_value'
    #def __init__(self,
    #             *args,
    #             **kwargs):
    #    super(TagUserDict,self).__init__(*args,**kwargs)
    def map_line_to_tag_user(self,key,line):
        if False:yield
        #user_tag_dict={}
        #Preprocessing
        for user_id,tag in ReadFile.read_json_yield_uid(line):
            yield tag,user_id
    def red_tag_user_to_dict(self,tag,user_ids):
        tag_user_dict={}
        freq_length=0
        total_freq=0
        for user_id in user_ids:
            tag_user_dict[str(user_id)]=tag_user_dict.get(str(user_id),0)+1
        for uid,freq in tag_user_dict.iteritems():
            freq_length+=(freq**2)
            total_freq+=freq
        freq_length=(freq_length**0.5)
        for uid,freq in tag_user_dict.iteritems():
            tag_user_dict[uid]=freq/freq_length
        yield tag,[tag,tag_user_dict,total_freq]
    def steps(self):
        return[self.mr(
                mapper=self.map_line_to_tag_user,\
                reducer=self.red_tag_user_to_dict
        )]
class UserTagDict1(MRJob):
    #DEFAULT_INPUT_PROTOCOL = 'raw_value'
    #def __init__(self,
    #             *args,
    #             **kwargs):
    #    super(UserTagDict,self).__init__(*args,**kwargs)
    def map_line_to_user_tag(self,key,line):
        if False:yield
        #user_tag_dict={}
        #Preprocessing
        for user_id,tag in ReadFile.read_json_yield_uid2(line):
            yield user_id,tag
    def red_user_tag_to_dict(self,user_id,tags):
        user_tag_dict={}
        for tag in tags:
            weight=1.01**(-tag[1]*0.5)
            user_tag_dict[tag[0]]=user_tag_dict.get(tag[0],0)+weight
        yield user_id,[user_id,user_tag_dict]
    def steps(self):
        return[self.mr(
                mapper=self.map_line_to_user_tag,\
                reducer=self.red_user_tag_to_dict
        )]
class TagUserDict1(MRJob):
    #DEFAULT_INPUT_PROTOCOL = 'raw_value'
    #def __init__(self,
    #             *args,
    #             **kwargs):
    #    super(TagUserDict,self).__init__(*args,**kwargs)
    def map_line_to_tag_user(self,key,line):
        if False:yield
        #user_tag_dict={}
        #Preprocessing
        for user_id,tag in ReadFile.read_json_yield_uid2(line):
            yield tag[0],[user_id,tag[1]]
    def red_tag_user_to_dict(self,tag,user_ids):
        tag_user_dict={}
        freq_length=0
        total_freq=0
        for user_id in user_ids:
            weight=1.01**(-user_id[1]*0.5)
            tag_user_dict[str(user_id[0])]=tag_user_dict.get(str(user_id[0]),0)+weight
        for uid,freq in tag_user_dict.iteritems():
            freq_length+=(freq**2)
            total_freq+=freq
        freq_length=(freq_length**0.5)
        for uid,freq in tag_user_dict.iteritems():
            tag_user_dict[uid]=freq/freq_length
        yield tag,[tag,tag_user_dict,total_freq]
    def steps(self):
        return[self.mr(
                mapper=self.map_line_to_tag_user,\
                reducer=self.red_tag_user_to_dict
        )]


class TrueCosine1(MRJob):
    #DEFAULT_INPUT_PROTOCOL = 'raw_value'
#retrieve the hashtaglist of all location
    def __init__(self,
#    #             min_hashtag_occurrences=MIN_HASHTAG_OCCURRENCES,
                 *args,
                 **kwargs):
        super(TrueCosine1, self).__init__(*args, **kwargs)
        self.hashtagdict=defaultdict(dict) 
    def map_hashtag_to_locFreq(self,key,line):
        if False:yield
        listt=cjson.decode(line) 
        for [uid,freq] in listt[1].iteritems():
            self.hashtagdict[uid][listt[0]]=freq
    def map_final_to_loc_dict(self):
        for uid,dictt in self.hashtagdict.iteritems():
            yield uid,dictt
    def red_to_hashtag_loc_freq(self, uid, dictts):
        completedict=defaultdict()
        for item in dictts:
            completedict.update(item)
        yield uid, completedict      
    def steps(self):
        return [self.mr(
                        mapper=self.map_hashtag_to_locFreq,\
                        mapper_final=self.map_final_to_loc_dict,\
                        reducer=self.red_to_hashtag_loc_freq
                )] 
class TrueCosine2(MRJob):
    #DEFAULT_INPUT_PROTOCOL = 'raw_value'
#retrieve the hashtaglist of all location
    def __init__(self,
#                 min_hashtag_occurrences=MIN_HASHTAG_OCCURRENCES,
                 *args,
                 **kwargs):
        super(TrueCosine2, self).__init__(*args, **kwargs)
        self.truecosine1=TrueCosine1()
    def map_neighbourdict_to_loc_dict(self,key,value):
        if False:yield
        for tag, freq in value.iteritems():
            for tag1,freq1 in value.iteritems():
                #if tag=='food' and tag1=='foodie':
                yield tag+'*'+tag1,freq*freq1
    def red_to_complete_loc_dict(self, key, value):
        cosinesum=0
        tags=key.split('*')
        tag1=tags[0]
        tag2=tags[1]
        for item in value:
            cosinesum=cosinesum+float(item)
           # completedict[loc1][loc2]=cosinesum #
#if use complete dict in this step, wont be able to get complete dictionay in the next function
#cause update a dictionary of dictionary using update will be totally wrong
        yield tag1,[tag1,tag2,cosinesum]
#        yield 'abc',completedict       
    def steps(self):
        return  self.truecosine1.steps()+\
                [self.mr(
                        mapper=self.map_neighbourdict_to_loc_dict,\
                #        mapper_final=self.map_final_to_loc_dict,\
                        reducer=self.red_to_complete_loc_dict
                )] 
#don't use TrueCosine3 any more!!
#cooccurence of tag pairs
class prob_step1(MRJob):
    def map_1(self, key,line):
        for keypair,value in ReadFile.read_utd_yield_tag_pair(line):
            yield keypair,value
    def reduce_1(self,key,value):
            yield key, sum(value)
    def steps(self):
        return [self.mr(
                        mapper=self.map_1,
                        reducer=self.reduce_1
                )]
class Lists(MRJob):
    def map_1(self, key,line):
        for listid,value in ReadFile.read_json_yield_list(line):
            yield listid,value
    def reduce_1(self,key,value):
        members=[]
        for cr,me in value:
            members.append(me)
        yield key,[key,cr,list(set(members))]
    def steps(self):
        return [self.mr(
                        mapper=self.map_1,
                        reducer=self.reduce_1
                )]

class Comember(MRJob):
    def map_1(self, key,line):
        line=line.split('\t')[1]
        line=cjson.decode(line)
        if len(line[-1])>1:
            for i in range(len(line[-1])):
                for j in range(i,len(line[-1])):
                    uid=line[-1][i]
                    uid1=line[-1][j]
                    if uid!=uid1:
                        yield str(uid)+'_'+str(uid1),1
    def reduce_1(self,key,value):
        yield key,sum(value)
    def steps(self):
        return [self.mr(
                        mapper=self.map_1,
                        reducer=self.reduce_1
                )]


if __name__=='__main__':
    #SiftTag.run()
    #SiftTagByTagger.run()
    #UserTagDict1.run()
    #TagUserDict1.run()
    #TrueCosine2.run()
    #prob_step1.run()
    #Lists.run()
    #Comember.run()
    #TagUserDict.run()
    UserTagDict.run()
