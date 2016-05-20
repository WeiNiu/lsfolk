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

    
    def parent_child_dict_from_gpd(self,gpd):
        # construct parent child dict from the graph parent dict.
        pcd=defaultdict(dict)
        for key,value in gpd:    
            pcd[key]['p']=value
            if 'c' not in pck[value[0]]:
                pcd[value[0]]['c']={}
            pcd[value[0]]['c'][key]=value[2]
        return pcd

    def rulelist_to_ruledict(self, rulelist):
        #for confidence base only since we can directly use cosine for centrality based.
        ruledict={}
        for line in open(rulelist,'r'):
            line=cjson.decode(line)
            key=line[0]+'_'+line[1]
            ruledict[key]=line[2]
        return ruledict

    def comp_candidate_order_strong(self, pcd, tfd, a_users_tag_dict,ruledict):
        #build a candidate sequency by strongest rule
        order=[]
        for tag in a_users_tag_dict:
            #add parent
            tag1=pcd[tag]['p'][0]
            if tag1 not in tag and tag1!='ROOT':
                key=tag+'_'+tag1
                key1=tag1+'_'+tag
                value=pcd[tag]['p'][1]
                order.append((tag1,value))
            #add sibling
            tag2=pcd[tag1]['c']
            for key,value in tag2.items():
                if key!=tag and key not in tag:
                    order.append((key,value))
            #add child
            if pcd[tag]['c']:
                for key,value in pcd[tag]['c'].items():
                    if key not in tag:
                        order.append((key,value))
        sorted(order,key=itemgetter(1),reverse=1)
        order=set(order)
        return order
    def comp_candidate_order_strong_most(self, pcd, tfd, a_users_tag_dict,ruledict):
        #build a candidate sequence by strongest rule of most voted tag
        order=[]
        for tag in sorted(a_users_tag_dict,key=itemgetter(1)):
            #add parent
            tag1=pcd[tag]['p'][0]
            if tag1 not in tag and tag1!='ROOT':
                key=tag+'_'+tag1
                key1=tag1+'_'+tag
                value=pcd[tag]['p'][1]
                if value>0.5:
                    order.append((tag1,value))
            #add child
            if pcd[tag]['c']:
                for key,value in pcd[tag]['c'].items():
                    if key not in tag and value>0.5:
                        order.append((key,value))
            #add sibling
            tag2=pcd[tag1]['c']
            for key,value in tag2.items():
                if key!=tag and key not in tag and value>0.5:
                    order.append((key,value))
        order=set(order)
        return order
    def comp_candidate_order_sim(self, pcd, tfd, a_users_tag_dict,ruledict):
        #build a candidate sequence by candidate similarity with existing tags all existing tag cnts.
        pass
    def comp_candidate_order_cnt(self, pcd, tfd, a_users_tag_dict,ruledict):
        #build a candidate sequence by candidate overall frequency
        order=[]
        for tag in a_users_tag_dict:
            #add parent
            tag1=pcd[tag]['p'][0]
            if tag1 not in tag and tag1!='ROOT':
                order.append((tag1,tfd[tag1])
            #add sibling
            tag2=pcd[tag1]['c']
            for key,value in tag2.items():
                if key!=tag and key not in tag:
                    order.append((key,tfd[key]))
            #add child
            if pcd[tag]['c']:
                for key,value in pcd[tag]['c'].items():
                    if key not in tag:
                        order.append((key,tfd[key]))
        sorted(order,key=itemgetter(1),reverse=1)
        order=set(order)
        return order
    def comp_candidate_order_mix(self, pcd, tfd, a_users_tag_dict,ruledict,alpha,beta):
        #build a candidate sequence by candidate overall frequency, rules, and most voted tag
        order=[]
        value2=a_user_tag_dict[tag]
        for tag in a_users_tag_dict:
            #add parent
            tag1=pcd[tag]['p'][0]
            if tag1 not in tag and tag1!='ROOT':
                key=tag+'_'+tag1
                key1=tag1+'_'+tag
                value0=pcd[tag]['p'][1]
                value1=tfd[tag1]
                mix=alpha*value0+beta*value1+(1-alpha-beta)*value2
                order.append((tag1,mix))
            #add sibling
            tag2=pcd[tag1]['c']
            for key,value in tag2.items():
                if key!=tag and key not in tag:
                    value1=tfd[key]
                    mix=alpha*value+beta*value1+(1-alpha-beta)*value2
                    order.append((key,mix))
            #add child
            if pcd[tag]['c']:
                for key,value in pcd[tag]['c'].items():
                    if key not in tag:
                        value1=tfd[key]
                        mix=alpha*value+beta*value1+(1-alpha-beta)*value2
                        order.append((key,mix))
        sorted(order,key=itemgetter(1),reverse=1)
        order=set(order)
        return order        

    def predict_a_user(self, ground_truth_a_user, tag_order_a_user, num_to_predict):
        for i in range(num_to_predict):
            accuracy=[]
            tag=tag_order_a_user[i][0]
            if tag in ground_truth_a_user:
                accuracy.append([1,ground_truth_a_user[tag]])
            else accuracy.append([0,0])
        return accuracy

    def predict_bulk(self,groud_truth,user_tag_dict,num_to_predict,pcd,tfd,ruledict):
        bulk_a=[]
        for user,ground_truth_a_user in groud_truth.iteritems():
            user_tag_dict_a_user=user_tag_dict[user]
            tag_order_a_user=comp_candidate_order_strong(self,pcd,tfd,user_tag_dict_a_user)
            accu=self.predict_a_user(ground_truth_a_user,tag_order_a_user,num_to_predict)
            bulk_a.append(accu)
        accuracy=[[0,0,0] for i in range(5)]
        for item in bulk_a:
            for v1,v2 in item:
                accuracy[0]+=1
                accuracy[1]+=v1
                accuracy[2]+=v2
        for item in accuracy:
            accuracy[item][1]/=accuracy[item][0]
            accuracy[item][2]/=accuracy[item][0]
        return accuracy


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
    
    gpd_file='../lc/gpd_hou'
    ground_truth_file='/Users/wei/Documents/folk_exp/backbone/validation1/user_tag_dict_hosuton1_selected'
    user_tag_dict_file='/Users/wei/Documents/folk_exp/backbone/validation1/user_tag_dict_hosuton_selected_part1'
    tag_freq_dict_file='/Users/wei/Documents/folk_exp/backbone/lc/tag_freq_dict_hou'
    rulelist_file='/Users/wei/Documents/folk_exp/centrality/lc/rulelist_tfidf_new_hou'

    #build ruledict
    ruledict=rulelist_to_ruledict(self, rulelist_file)
    #build parent child dict
    pcd=parent_child_dict_from_gpd(gpd)
    #read in tfd
    tfd_file=open(tag_freq_dict_file,'r')
    tfd=cjson.decode(tfd_file)

    user_tag_dict={}
    ground_truth=defaultdict(dict)
    for line in open(user_tag_dict_file,'r'):
        line=cjson.decode(line)
        user_tag_dict[line[0]]=line[1]
    for line in open(ground_truth_file,'r'):
        line=cjson.decode(line)
        ground_truth[line[0]]=line[1]    

    acc=data.predict_bulk(ground_truth,user_tag_dict,5, pcd, tfd, ruledict)# dict, dict, int, dict, dict, dict

    outfile=open('test_acc','w')
    print >>outfile, acc 




    #data.data_prepration(4,'../user_tag_dict_all1')
    #data.data_prepration(4,sys.argv[1])
    #docs=['../user_tag_dict_all1_fold1','../user_tag_dict_all1_fold2','../user_tag_dict_all1_fold3','../user_tag_dict_all1_fold4']
    #data.construct_training(['user_tag_dict_houston1_fold1','user_tag_dict_houston1_fold2','user_tag_dict_houston1_fold3'],4)
    #data.nfold_(4,docs)
    #data.prediction_by_parent_child('./rulelist3_houston_train_1','user_tag_dict_houston1_fold1','user_tag_dict_houston1_train_1')
    #data.prediction_by_centrality_strong(sys.argv[1],sys.argv[2],sys.argv[3]) 
    #data.prediction_by_centrality_most(sys.argv[1],sys.argv[2],sys.argv[3])    
    #data.prediction_by_strong_rule(sys.argv[1],sys.argv[2],sys.argv[3])
    #data.prediction_by_strong_rule_of_most_voted_tag(sys.argv[1],sys.argv[2],sys.argv[3])

    #data.prediction_by_major_topic(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])
