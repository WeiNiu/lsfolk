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
#from library.geo import getHaversineDistance
from copy import deepcopy
import re
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
        for tag in tags:
            yield user_id,tag
    @staticmethod
    def read_json_yield_tag(line):
        line = cjson.decode(line)
        user_id=line['user_id']
        tags=line['tag']
        for tag in tags:
            line1=deepcopy(line)
            line1['tag']=[tag]
            yield tag,line1
######################################
# No corpus.stopword exist on server #
# Try single thread version on rex   #
######################################

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

class TagUserDict(ModifiedMRJob):
    DEFAULT_INPUT_PROTOCOL = 'raw_value'
    def __init__(self,
                 *args,
                 **kwargs):
        super(TagUserDict,self).__init__(*args,**kwargs)
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

class TrueCosine1(ModifiedMRJob):
    DEFAULT_INPUT_PROTOCOL = 'raw_value'
#retrieve the hashtaglist of all location
    def __init__(self,
#                 min_hashtag_occurrences=MIN_HASHTAG_OCCURRENCES,
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
class TrueCosine2(ModifiedMRJob):
    DEFAULT_INPUT_PROTOCOL = 'raw_value'
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
        return   self.truecosine1.steps()+\
                [self.mr(
                        mapper=self.map_neighbourdict_to_loc_dict,\
                #        mapper_final=self.map_final_to_loc_dict,\
                        reducer=self.red_to_complete_loc_dict
                )] 
'''don't use TrueCosine3 any more!!
class TrueCosine3(ModifiedMRJob):
    DEFAULT_INPUT_PROTOCOL = 'raw_value'
#retrieve the hashtaglist of all location
    def __init__(self,
#                 min_hashtag_occurrences=MIN_HASHTAG_OCCURRENCES,
                 *args,
                 **kwargs):
        super(TrueCosine3, self).__init__(*args, **kwargs)
        self.truecosine2=TrueCosine2()
        self.locdict=defaultdict(dict)
    def map_neighbourdict_to_loc_dict(self,key,value):
        self.locdict[key][value[0]]=value[1]
        #self.locdict[value[0]][key]=value[1]
    def map_final_dict(self):
        yield 'abc',self.locdict
    def red_to_complete_loc_dict(self, key, value):
        completedict={}
        for item in value:
            completedict.update(item)
        yield 'abc',completedict      
    def steps(self):
        return   self.truecosine2.steps()+\
                [self.mr(
                        mapper=self.map_neighbourdict_to_loc_dict,\
                        mapper_final=self.map_final_dict,\
                        reducer=self.red_to_complete_loc_dict
                )] 
'''

class TagCooccur(ModifiedMRJob):
    DEFAULT_INPUT_PROTOCOL = 'raw_value'
    def __init__(self,
                 *args,
                 **kwargs):
        super(TagCooccur,self).__init__(*args,**kwargs)
        self.tag_co_dict=defaultdict(dict)
    def map_line_to_user_tag(self,key,line):
        if False:yield
        line=cjson.decode(line)
        for key,value in line[1].iteritems():
            for key1,value1 in line[1].iteritems():
                if key!=key1:
                    #t=[key,key1]
                    #t1=sorted(t)
                    #yield str(t1[0])+'_'+str(t1[1]),1
                   # yield str(t1[0])+'_'+str(t1[1]),min(value,value1)
                    self.tag_co_dict[key][key1]=min(value,value1)
                    self.tag_co_dict[key1][key]=min(value,value1)
                else:continue
    def map_final(self):
        for key,value in self.tag_co_dict.iteritems():
            yield key,value
    def red_user_tag_to_dict(self,tag,value):
        #finaldict=defaultdict(dict)
        a=merge_dict(value)
        yield tag,[tag,a]
        
    #    yield tag,[tag,sum(value)] 
    def steps(self):
        return[self.mr(
                mapper=self.map_line_to_user_tag,\
                mapper_final=self.map_final,\
                reducer=self.red_user_tag_to_dict
        )]

if __name__ == '__main__':
    #Preprocessing.run()
    #UserTagDict.run()
    #TagUserDict.run()
    #TrueCosine1.run()
    TrueCosine2.run()
    #TrueCosine3.run()
    #TopicRank.run()
    #TagCooccur.run()
    #SiftTag.run()

