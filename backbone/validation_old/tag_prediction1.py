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

name=['chi','ny','la','sf','hou','miami','london','sydney','seattle','dallas']
target_loc=[[41.84,-87.68],[40.71,-73],[34.05,-118.24],[37.77,-122.42],[29.76,-95.36],[25.76,-80.19],[33.74,-84.38],[39.95,-75.16],[47.6,-122.3],[32.77,-96.8]]

class TagPrediction(object):
    def data_prepration(self,nfold,data_file):#user_tag_dict_1
        outfile=[]
        #tagdict=[]
        for i in range(nfold):
            outfile.append(open(data_file+'_fold'+str(i+1),'w'))
            
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
        outfile=open(infile+'_train_'+str(xfold),'w')
        for filename in infiles:
            files.append(open(filename,'r'))
        
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
    def prediction_by_strong_rule_of_most_voted_tag(self,rulelistfile,ground_truth_file,user_tag_dict_file):
        #order the rules for each tag in a list of list
        user_tag_dict={}
        ground_truth=defaultdict(dict)
        rule_by_tag=defaultdict(list)
        for line in open(user_tag_dict_file,'r'):
            line=cjson.decode(line)
            user_tag_dict[line[0]]=line[1]
        for line in open(ground_truth_file,'r'):
            line=cjson.decode(line)
            ground_truth[line[0]]=line[1]
        for line in open(rulelistfile,'r'):
            line=cjson.decode(line)
            if line[2]>0.5:
                rule_by_tag[line[0]].append(line)
        no1=0
        for key in rule_by_tag:
            rule_by_tag[key]=sorted(rule_by_tag[key],key=itemgetter(2),reverse=1)
            #print rule_by_tag[key][0][2]
            #if rule_by_tag[key][0][2]==1:
            #    no1+=1
            
        cnt=0
        cntt=0
        cntp=0
        cntx=0
        for user,utd in user_tag_dict.iteritems():     
            utd1=sorted(utd.items(),key=itemgetter(1),reverse=1)
            utd1=list(utd1)
            #print utd1
            if utd and utd1[0][1]==1:
                no1+=1
            found=False
            while found==False:
                for item in utd1:
                    if item[0] in rule_by_tag:
                        rules=rule_by_tag[item[0]]
                        for rule in rules:
                            if rule[1] not in utd:
                                #print user,rule[1]
                                cnt+=1
                                if rule[1] in ground_truth[user]:
                                    cntt+=1
                                    #print user,rule
                                    #for key,value in ground_truth[user]:
                                    
                                    cntp+=ground_truth[user][rule[1]]
                                    #if user=='34272713':
                                    #print user,rule
                                else:
                                    #if user==34272713:
                                    #print user,rule
                                    pass
                                found=True
                                #print user,rule
                                break
                            else:
                                continue
                    if found==True:
                        break        
                    else:
                        continue
                break
        print cnt,cntt,cntp,no1
    

    
    def prediction_by_strong_rule(self,rulelistfile,ground_truth_file,user_tag_dict_file):
        #order the rules of existing tag in decreasing order in one list.
        user_tag_dict={}
        ground_truth=defaultdict(dict)
        rule_by=defaultdict(list)
        for line in open(user_tag_dict_file,'r'):
            line=cjson.decode(line)
            user_tag_dict[line[0]]=line[1]
        for line in open(ground_truth_file,'r'):
            line=cjson.decode(line)
            ground_truth[line[0]]=line[1]
        for line in open(rulelistfile,'r'):
            line=cjson.decode(line)
            if line[2]>0.5:
                rule_by[line[0]].append(line)
        for key in rule_by:
            rule_by[key]=sorted(rule_by[key],key=itemgetter(2),reverse=1)
        #print rule_by[1]
        cnt=0
        cntt=0
        cntp=0
        for user,utd in user_tag_dict.iteritems():
            #utd1=sorted(utd.items(),key=itemgetter(1),reverse=1)
            rule_combo=[]
            for key in utd:
                rule_combo+=rule_by[key]
            rule_combo=sorted(rule_combo,key=itemgetter(2,3),reverse=1)
            found=False
            while found==False:
                for rule in rule_combo:
                    if rule[1] not in utd:
                                #print user,rule[1]
                        cnt+=1
                        if rule[1] in ground_truth[user]:
                            cntt+=1
                            cntp+=ground_truth[user][rule[1]]
                                    #print user,rule
                        else:
                                    #print user,rule
                            pass
                        found=True
                        break
                    else:
                        continue
                break
        print cnt,cntt,cntp

    def prediction_by_major_topic(self,rulelistfile,ground_truth_file,user_tag_dict_file,tfd,cosine):
        #def prediction_by_strong_rule(self,rulelistfile,ground_truth_file,user_tag_dict_file):
        #order the rules of existing tag in decreasing order in one list.
        user_tag_dict={}
        ground_truth=defaultdict(dict)
        rule_by=defaultdict(list)
        rule_by1=defaultdict(dict)
        #candidate=[]
        for line in open(user_tag_dict_file,'r'):
            line=cjson.decode(line)
            user_tag_dict[line[0]]=line[1]
        for line in open(ground_truth_file,'r'):
            line=cjson.decode(line)
            ground_truth[line[0]]=line[1]
        for line in open(rulelistfile,'r'):
            line=cjson.decode(line)
            if line[2]>0.5:
                rule_by[line[0]].append(line)
            
            rule_by1[line[0]][line[1]]=line[2]
        tagfile=open(tfd,'r')
        tfd=cjson.decode(tagfile.readline())
        cosine=open(cosine,'r')
        cosine=cjson.decode(cosine.readline())
        #    if line[0] in ground_truth and line[1] not in groud_truth and line[2]>0.5:
        #    rule_by[line[0]].append(line)
        #candidate.append(line[1])
        #for key in rule_by:
        #    rule_by[key]=sorted(rule_by[key],key=itemgetter(2),reverse=1)
        #print rule_by[1]
        cnt=0
        cntt=0
        cntp=0
        for user,utd in user_tag_dict.iteritems():
            candidate=[]
            for key in utd:
                for rule in rule_by[key]:
                    if rule[1] not in utd:
                        candidate.append([rule[0],rule[1]])
            canscore=[]
            for can in candidate:
                score=0
                for item in utd:
                    cosinev=cosine.get(can+'_'+item,0)
                    cosineq=cosine.get(item+'_'+can,0)
                    score+=(cosinev+consineq)*log(utd[item])
                #lets use  sum(sim(k,j)*log(f(j)))
                canscore.append([can[1],score])
                #print canscore
                #print ground_truth[user]
            if canscore!=[]:
                tag=sorted(canscore,key=itemgetter(1),reverse=1)[0]
                #print tag 
                cnt+=1
            
                if tag[0] in ground_truth[user]:
                    cntt+=1
                    cntp+=ground_truth[user][tag[0]]
        print cnt,cntt,cntp



    def prediction_by_parent_child(self,rulelistfile,ground_truth_file,user_tag_dict_file):
        #identify major topic
        user_tag_dict={}
        ground_truth=defaultdict(dict)
        rule_by_tag=defaultdict(list)
        for line in open(user_tag_dict_file,'r'):
            line=cjson.decode(line)
            user_tag_dict[line[0]]=line[1]
        for line in open(ground_truth_file,'r'):
            line=cjson.decode(line)
            ground_truth[line[0]]=line[1]
        for line in open(rulelistfile,'r'):
            line=cjson.decode(line)
            if line[2]>0.7:
                rule_by_tag[line[0]].append([line[1],line[2],line[3]])
                rule_by_tag[line[1]].append([line[0],line[2],line[3]])
        no1=0
        for key in rule_by_tag:
            rule_by_tag[key]=sorted(rule_by_tag[key],key=itemgetter(1),reverse=1)
            #print rule_by_tag[key][0][2]
            #if rule_by_tag[key][0][2]==1:
            #    no1+=1
            
        cnt=0
        cntt=0
        cntp=0
        for user,utd in user_tag_dict.iteritems():
            #print user
            #if user==34272713:
            #    print utd 
            utd1=sorted(utd.items(),key=itemgetter(1),reverse=1)
            utd1=list(utd1)
            print utd1
            if utd and utd1[0][1]==1:
                no1+=1
            found=False
            while found==False:
                for item in utd1:
                    if item[0] in rule_by_tag:
                        rules=rule_by_tag[item[0]]
                        for rule in rules:
                            if rule[0] not in user_tag_dict:
                                #print user,rule[1]
                                cnt+=1
                                if rule[0] in ground_truth[user]:
                                    cntt+=1
                                    cntp+=ground_truth[user][rule[0]]
                                    #if user=='34272713':

                                    #print user,rule
                                else:
                                    #if user==34272713:
                                    print user,rule
                                    pass
                                found=True
                                break
                            else:
                                continue
                        break        
                    else:
                        continue
                break
        print cnt,cntt,cntp,no1
        pass
    
    def prediction_by_centrality_most(self,rulelistfile,ground_truth_file,user_tag_dict_file):
        user_tag_dict={}
        ground_truth=defaultdict(dict)
        rule_by_tag=defaultdict(list)
        for line in open(user_tag_dict_file,'r'):
            line=cjson.decode(line)
            user_tag_dict[line[0]]=line[1]
        for line in open(ground_truth_file,'r'):
            line=cjson.decode(line)
            ground_truth[line[0]]=line[1]
        for line in open(rulelistfile,'r'):
            line=cjson.decode(line)
            if line[2]>0.5:
                rule_by_tag[line[0]].append(line)
        no1=0
        for key in rule_by_tag:
            rule_by_tag[key]=sorted(rule_by_tag[key],key=itemgetter(2),reverse=1)
            #print rule_by_tag[key][0][2]
            #if rule_by_tag[key][0][2]==1:
            #    no1+=1
            
        cnt=0
        cntt=0
        cntp=0
        cntx=0
        for user,utd in user_tag_dict.iteritems():     
            utd1=sorted(utd.items(),key=itemgetter(1),reverse=1)
            utd1=list(utd1)
            #print utd1
            if utd and utd1[0][1]==1:
                no1+=1
            found=False
            while found==False:
                for item in utd1:
                    if item[0] in rule_by_tag:
                        rules=rule_by_tag[item[0]]
                        for rule in rules:
                            if rule[1] not in utd:
                                print user,rule[1]
                                cnt+=1
                                if rule[1] in ground_truth[user]:
                                    cntt+=1
                                    print user,'---',rule
                                    #for key,value in ground_truth[user]:
                                    
                                    cntp+=ground_truth[user][rule[1]]
                                    #if user=='34272713':
                                    #print user,rule
                                else:
                                    #if user==34272713:
                                    #print user,rule
                                    pass
                                found=True
                                #print user,rule
                                break
                            else:
                                continue
                    if found==True:
                        break        
                    else:
                        continue
                break
        print cnt,cntt,cntp,no1
    def prediction_by_centrality_strong(self,rulelistfile,ground_truth_file,user_tag_dict_file):
        user_tag_dict={}
        ground_truth=defaultdict(dict)
        rule_by=defaultdict(list)
        for line in open(user_tag_dict_file,'r'):
            line=cjson.decode(line)
            user_tag_dict[line[0]]=line[1]
        for line in open(ground_truth_file,'r'):
            line=cjson.decode(line)
            ground_truth[line[0]]=line[1]
        for line in open(rulelistfile,'r'):
            line=cjson.decode(line)
            if line[2]>0.5:
                rule_by[line[0]].append(line)
        for key in rule_by:
            rule_by[key]=sorted(rule_by[key],key=itemgetter(2),reverse=1)
        #print rule_by[1]
        cnt=0
        cntt=0
        cntp=0
        for user,utd in user_tag_dict.iteritems():
            #utd1=sorted(utd.items(),key=itemgetter(1),reverse=1)
            rule_combo=[]
            for key in utd:
                rule_combo+=rule_by[key]
            rule_combo=sorted(rule_combo,key=itemgetter(2),reverse=1)
            found=False
            while found==False:
                for rule in rule_combo:
                    if rule[1] not in utd:
                                #print user,rule[1]
                        cnt+=1
                        if rule[1] in ground_truth[user]:
                            cntt+=1
                            cntp+=ground_truth[user][rule[1]]
                                    #print user,rule
                        else:
                                    #print user,rule
                            pass
                        found=True
                        break
                    else:
                        continue
                break
        print cnt,cntt,cntp

if __name__ =='__main__':
    data=TagPrediction()
    #data.data_prepration(4,'../user_tag_dict_all1')
    #data.data_prepration(4,sys.argv[1])
    #docs=['../user_tag_dict_all1_fold1','../user_tag_dict_all1_fold2','../user_tag_dict_all1_fold3','../user_tag_dict_all1_fold4']
    #data.construct_training(['user_tag_dict_houston1_fold1','user_tag_dict_houston1_fold2','user_tag_dict_houston1_fold3'],4)
    #data.nfold_(4,docs)
    #data.prediction_by_parent_child('./rulelist3_houston_train_1','user_tag_dict_houston1_fold1','user_tag_dict_houston1_train_1')
    #data.prediction_by_centrality_strong(sys.argv[1],sys.argv[2],sys.argv[3]) 
    #data.prediction_by_centrality_most(sys.argv[1],sys.argv[2],sys.argv[3])    
    #data.prediction_by_strong_rule(sys.argv[1],sys.argv[2],sys.argv[3])
    data.prediction_by_strong_rule_of_most_voted_tag(sys.argv[1],sys.argv[2],sys.argv[3])

    #data.prediction_by_major_topic(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])
