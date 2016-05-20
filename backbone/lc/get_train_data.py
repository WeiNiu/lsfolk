from __future__ import division
import cjson
import sys
from operator import itemgetter

user_tag_dict_all_f=sys.argv[2]
user_tag_dict_all={}
for line in open(user_tag_dict_all_f,'r'):
    line=cjson.decode(line)
    user_tag_dict_all[line[0]]=line[1]
#delete the users for prediction from all
#user_tag_dict_g={}#ground truth
#for key in user_tag_dict_p:
#    user_tag_dict_g[key]=user_tag_dict_all[key]
    #del user_tag_dict_all[key]
#    user_tag_dict_all[key]=user_tag_dict_p[key]


user_tag_dict_to_predict=sys.argv[1]
#user_tag_dict_p={}
for line in open(user_tag_dict_to_predict,'r'):
    line=cjson.decode(line)
    user_tag_dict_all[line[0]]=line[1]



traindata=sys.argv[3] 
outfile=open(traindata,'w')
for key,value in user_tag_dict_all.iteritems():

    outfile.write(cjson.encode([key,value])+'\n')

tagdictfile=sys.argv[4]
readtagdictfile=open(sys.argv[4],'r')
line=cjson.decode(readtagdictfile.readline())


taglistfile=sys.argv[5]
outfile1=open(taglistfile,'w')
outfile1.write(cjson.encode(line.keys())) 
print len(line)

