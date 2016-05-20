#include tag count
from __future__ import division
import cjson
from collections import defaultdict,deque
from operator import itemgetter
import sys
from copy import deepcopy
from math import log,log10
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

rlist=['social medium', 'medium', 'social', 'twibe marketing', 'twibe']
class TagPrediction(object):
    def __init__(self):
        self.pred=''
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
        for key,value in gpd.items():    
            pcd[key]['p']=value
            if 'c' not in pcd[value[0]]:
                pcd[value[0]]['c']={}
            pcd[value[0]]['c'][key]=value[1]
        return pcd

    def rulelist_to_ruledict(self, rulelist):
        #for confidence base only since we can directly use cosine for centrality based.
        ruledict={}
        for line in open(rulelist,'r'):
            line=cjson.decode(line)
            key=line[0]+'_'+line[1]
            ruledict[key]=line[2]
        return ruledict

    def comp_candidate_order_strong(self, pcd, tfd, a_users_tag_dict,ruledict,removelist):
        #build a candidate sequency by strongest rule
        order=[]
        for tag in a_users_tag_dict:
            #add parent
            if tag in removelist or tag not in tfd:
                continue
            tag1=pcd[tag]['p'][0]
            if tag1 not in tag and tag1!='ROOT' and tag1 not in a_users_tag_dict:
#                key=tag+'_'+tag1
#                key1=tag1+'_'+tag
                value=pcd[tag]['p'][1]
                order.append((tag1,value))
            #add sibling
            tag2=pcd[tag1]['c']
            for key,value in tag2.items():
                if key!=tag and key not in tag and key not in a_users_tag_dict:
                    k=tag+'_'+key
                    k1=key+'_'+tag
                    sim=ruledict.get(k,0)+ruledict.get(k1,0)
                    order.append((key,sim))
            #add child
            if 'c' in pcd[tag]:
                for key,value in pcd[tag]['c'].items():
                    if key not in tag and key not in a_users_tag_dict:
                        order.append((key,value))
        order=set(order)
        order=sorted(order,key=itemgetter(1),reverse=1)
        return order,1
    def comp_candidate_order_strong_most(self, pcd, tfd, a_users_tag_dict,ruledict,removelist):
        #build a candidate sequence by strongest rule of most voted tag
        order1=[]
        listt=sorted(a_users_tag_dict.items(),key=itemgetter(1),reverse=1)
        print listt,'```'
        for tag,f in listt:
            order=[]
            #add parent
            if tag in removelist or tag not in tfd:
                continue
            #print tag,pcd[tag]
            tag1=pcd[tag]['p'][0]
            #print tag1
            if tag1 not in tag and tag1!='ROOT'and tag1 not in a_users_tag_dict:
                key=tag+'_'+tag1
                key1=tag1+'_'+tag
                value=pcd[tag]['p'][1]
                if value>0.5:
                    order.append((tag1,value))
            #add child
            if 'c' in pcd[tag]:
                for key,value in pcd[tag]['c'].items():
                    if key not in tag and value>0.5  and key not in a_users_tag_dict:
                        order.append((key,value))
            #add sibling
            tag2=pcd[tag1]['c']
            for key,value in tag2.items():
                k=tag+'_'+key
                k1=key+'_'+tag
                sim=ruledict.get(k,0)+ruledict.get(k1,0)
                if key!=tag and key not in tag and sim>0.5 and key not in a_users_tag_dict:
                    order.append((key,sim))
            #print order
            order1+=sorted(order,key=itemgetter(1),reverse=1)
            #print 'ss',order
        #order1=set(order1)
        #print order1
        return order1,1
    def comp_candidate_order_sim(self, pcd, tfd, a_users_tag_dict,ruledict,removelist):
        #build a candidate sequence by candidate similarity with existing tags all existing tag cnts.
        pass
    def comp_candidate_order_cnt(self, pcd, tfd, a_users_tag_dict,ruledict,removelist):
        #build a candidate sequence by candidate overall frequency
        order=[]
        for tag in a_users_tag_dict:
            #add parent
            if tag in removelist or tag not in tfd:
                continue
            tag1=pcd[tag]['p'][0]
            if tag1 not in tag and tag1!='ROOT'and tag1 not in a_users_tag_dict:
                order.append((tag1,tfd[tag1]))
            #add sibling
            tag2=pcd[tag1]['c']
            for key,value in tag2.items():
                if key!=tag and key not in tag and key not in a_users_tag_dict:
                    order.append((key,tfd[key]))
            #add child
            if 'c' in pcd[tag]:
                for key,value in pcd[tag]['c'].items():
                    if key not in tag and key not in a_users_tag_dict:
                        order.append((key,tfd[key]))
        order=set(order)
        order=sorted(order,key=itemgetter(1),reverse=1)
        #print order
        return order,1
    def comp_candidate_order_mix(self, pcd, tfd, a_users_tag_dict,ruledict,removelist):
        #build a candidate sequence by candidate overall frequency, rules, and most voted tag
        order=[]
        cntlist=[]
        for tag in a_users_tag_dict:
            cnt=1
            value2=a_users_tag_dict[tag]
            #add parent
            if tag in removelist or tag not in tfd:
                continue
            print pcd[tag],tag
            tag1=pcd[tag]['p'][0]
            if tag1 not in tag and tag1!='ROOT' and tag1 not in a_users_tag_dict and tag1 not in rlist:
                #key=tag+'_'+tag1
                #key1=tag1+'_'+tag
                value0=pcd[tag]['p'][1]
                value1=tfd[tag1]
                #mix=value0*(log(value1))
                mix=value0*(log(value1)+log(value2))
                #mix=alpha*value0+beta*value1+(1-alpha-beta)*value2
                order.append((tag1,mix))
            #add sibling
            tag2=pcd[tag1]['c']
            for key,value in tag2.items():
                if key!=tag and key not in tag and key not in a_users_tag_dict and key not in rlist:
                    k=tag+'_'+key
                    k1=key+'_'+tag
                    sim=ruledict.get(k,0)+ruledict.get(k1,0)
                    value1=tfd[key]
                    #mix=sim*(log(value1))
                    mix=sim*(log(value1)+log(value2))
                    #mix=alpha*value+beta*value1+(1-alpha-beta)*value2
                    order.append((key,mix))
            if tag1 != 'ROOT':
                cnt+=len(tag2)-1
            #add child
            if 'c' in pcd[tag]:
                for key,value in pcd[tag]['c'].items():
                    if key not in tag and key not in a_users_tag_dict and key not in rlist:
                        value1=tfd[key]
                        #mix=value*(log(value1))
                        mix=value*(log(value1)+log(value2))
                        #mix=alpha*sim+beta*value1+(1-alpha-beta)*value2
                        order.append((key,mix))
                cnt+=len(pcd[tag]['c'])
        #order=set(order)
            cntlist.append(cnt)
        order=sorted(order,key=itemgetter(1),reverse=1)
        avg=sum(cntlist)/len(cntlist)
        return order,avg        

    def predict_a_user(self, ground_truth_a_user, tag_order_a_user, num_to_predict):
        accuracy=[]
        tag_order_a_user=list(tag_order_a_user)
        #lengthorder=len(tag_order_a_user)
        #print tag_order_a_user
        if len(tag_order_a_user)<num_to_predict:
            return None
        for i in range(num_to_predict):

            tag=tag_order_a_user[i][0]
            tg=tag.replace(' ','-')
            self.pred+=tg
            self.pred+=' '
            if tag in ground_truth_a_user:
                #print tag,ground_truth_a_user[tag]
                accuracy.append([1,ground_truth_a_user[tag]])

            else: accuracy.append([0,0])
        #print accuracy
        return accuracy

    def predict_bulk(self,groud_truth,user_tag_dict,num_to_predict,pcd,tfd,ruledict,removelist):
        bulk_a=[]
        cntlist=[]
        for user,ground_truth_a_user in groud_truth.iteritems():
            user_tag_dict_a_user=user_tag_dict[user]
            tag_order_a_user,avg=self.comp_candidate_order_mix(pcd,tfd,user_tag_dict_a_user,ruledict,removelist)
            #print tag_order_a_user
            accu=self.predict_a_user(ground_truth_a_user,tag_order_a_user,num_to_predict)
            if accu!=None:
                bulk_a.append(accu)
                cntlist.append(avg)
        accuracy=[[0,0,0] for i in range(5)]
        for item in bulk_a:
            for i in range(len(item)):
                accuracy[i][0]+=1
                accuracy[i][1]+=item[i][0]
                accuracy[i][2]+=item[i][1]
        for i in range(len(accuracy)):
            accuracy[i][1]/=accuracy[i][0]
            accuracy[i][2]/=accuracy[i][0]
        cost=sum(cntlist)/len(cntlist)
        return accuracy,cost




if __name__ =='__main__':
    data=TagPrediction()
    
    gpd_file=sys.argv[1]#'/Users/wei/Documents/folk_exp/centrality/graph/gpd2_hou'
    ground_truth_file=sys.argv[2]#'/Users/wei/Documents/folk_exp/backbone/validation/user_tag_dict_houston_selected'
    user_tag_dict_file=sys.argv[3]#'/Users/wei/Documents/folk_exp/backbone/validation/user_tag_dict_houston_selected_part1'
    tag_freq_dict_file=sys.argv[4]#'/Users/wei/Documents/folk_exp/backbone/lc/tag_freq_dict_hou'
    rulelist_file=sys.argv[5]#'/Users/wei/Documents/folk_exp/centrality/lc/rulelist_tfidf_new_hou'
    removelist=sys.argv[6]#'/Users/wei/Documents/folk_exp/backbone/lc/removelist_hou'

    removelist=open(removelist,'r')
    removelist=cjson.decode(removelist.readline())

    gpd_file=open(gpd_file,'r')
    gpd=cjson.decode(gpd_file.readline())

    #build ruledict
    ruledict=data.rulelist_to_ruledict(rulelist_file)
    #build parent child dict
    pcd=data.parent_child_dict_from_gpd(gpd)
    #read in tfd
    tfd_file=open(tag_freq_dict_file,'r')
    tfd=cjson.decode(tfd_file.readline())

    user_tag_dict={}
    ground_truth=defaultdict(dict)
    for line in open(user_tag_dict_file,'r'):
        line=cjson.decode(line)
        user_tag_dict[line[0]]=line[1]
    for line in open(ground_truth_file,'r'):
        line=cjson.decode(line)
        ground_truth[line[0]]=line[1]    

    acc=data.predict_bulk(ground_truth,user_tag_dict,5, pcd, tfd, ruledict,removelist)# dict, dict, int, dict, dict, dict

    outfile=open(sys.argv[7],'w')
    print >>outfile, acc 

    outfilex=open('tags-old','a')
    outfilex.write(data.pred)


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
