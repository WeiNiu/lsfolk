from __future__ import division
import cjson
import sys
from operator import itemgetter
user_tag_dict_to_predict=sys.argv[1]
user_tag_dict_p={}
for line in open(user_tag_dict_to_predict,'r'):
    line=cjson.decode(line)
    user_tag_dict_p[line[0]]=line[1]

user_tag_dict_all_f=sys.argv[2]
user_tag_dict_all={}
for line in open(user_tag_dict_all_f,'r'):
    line=cjson.decode(line)
    user_tag_dict_all[line[0]]=line[1]
#delete the users for prediction from all
user_tag_dict_g={}#ground truth
for key in user_tag_dict_p:
    user_tag_dict_g[key]=user_tag_dict_all[key]
    #del user_tag_dict_all[key]
    user_tag_dict_all[key]=user_tag_dict_p[key]
accuracy=[]
tlist=['social medium', 'social', 'medium', 'twibe', 'twibe-marketing']
pred=''
for key,value in user_tag_dict_p.iteritems():
    similarity={}
    setp=set(user_tag_dict_p[key].keys())
    for key1,value1 in user_tag_dict_all.iteritems():
        set1=set(user_tag_dict_all[key1].keys())
        inter=setp.intersection(set1)
        length=len(inter)
        similarity[key1]=length
        #print inter
    top10=sorted(similarity.items(),key=itemgetter(1),reverse=1)[2:11]
    #aggregate top 10 tags
    #print top10
    top10agg={}
    
    for users,sim in top10:
        y=user_tag_dict_all[users]
        top10agg={ k: top10agg.get(k, 0) + y.get(k, 0) for k in set(top10agg) | set(y) }
       
        topredict=sorted(top10agg.items(),key=itemgetter(1),reverse=1)
        #print topredict
        cnt=0
        accu=[]
        for tag in topredict:
            #print tag,key
            #print user_tag_dict_p[key]
            #print user_tag_dict_g[key]
            if cnt>=5:
                break
            if tag[0] not in user_tag_dict_p[key] and tag[0]not in tlist:
                cnt+=1
                tg=tag[0].replace(" ", "-")
                pred+=tg
                pred+=' '
                if tag[0] in user_tag_dict_g[key]:
                    accu.append([1,user_tag_dict_g[key][tag[0]]])
                else:
                    accu.append([0,0])
    accuracy.append(accu)
outfile=open(sys.argv[3],'w')
#acc=[0,0]*5
accu=[[0,0,0] for i in range(5)]
for item in accuracy:
    for i in range(len(item)):
        accu[i][0]+=1
        accu[i][1]+=item[i][0]
        accu[i][2]+=item[i][1]

for i in range(len(accu)):
        accu[i][1]/=accu[i][0]
        accu[i][2]/=accu[i][0]
#cost=sum(cntlist)/len(cntlist)
    

outfile.write(cjson.encode(accu))
outfile1=open('tags','a')
outfile1.write(pred)

