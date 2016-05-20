#converting key from user to tags
from __future__ import division
import cjson
import sys
from collections import defaultdict
# args: user_tag_dict    tag-tag-dict
#filename='/spare/wei/folk/user_tag_dict_nonsingular_100_10'
filename=sys.argv[1]#'/spare/wei/local/user_tag_dict_ch3'#'/spare/wei/user_tag_dict_l1'#'/spare/wei/folk/user_tag_dict_en_lt10_for_prob_1_3'#'/spare/wei/folk/user_tag_dict_en_for_prob'#user_tag_dict_greater_than_3000'
#filename='/spare/wei/folk/user_tag_dict_ny_u5_10'
#outfile='/spare/wei/links'
#out=open(outfile,'w')
outfile1=sys.argv[2]#'/spare/wei/local/tag-tag-dict_ch3'#'./link-dict_en_lt10_3'
#outfile1='./link-dict_ny_u5_10'
out1=open(outfile1,'w')
tag_dict={}
unique_tags=[]
for line in open(filename):
    #line=line.split('\t')[1]
    tagdict = cjson.decode(line)[1]
    for tag,value in tagdict.iteritems():
        if tag not in unique_tags:
            unique_tags.append(tag)
        for tag1,value1 in tagdict.iteritems():
            if tag != tag1 and tag1+'_'+tag not in tag_dict and min(value,value1)>1:
                tag_dict[tag+'_'+tag1]=min(value1,value)+tag_dict.get(tag+'_'+tag1,0)
#                tag_dict[tag+'_'+tag1]=
            elif tag==tag1:
                tag_dict[tag+'_'+tag1]=value+tag_dict.get(tag+'_'+tag,0)
#                tag_dict[tag1][tag]=1+tag_dict[tag1].get(tag,0)
            else:pass
out1.write(cjson.encode(tag_dict)) 

#out2='uni_tag'
#out2=open(out2,'w')
#out2.write(cjson.encode(unique_tags))
#print '_____1_____'
#for key,value in tag_dict.iteritems():
#    for key1,value1 in value.iteritems():
#        tagdict[key][key1]=tagdict[key][key1]/tagdict[key][key]
#print '_____2_____'
#for key,value in tag_dict.iteritems():
#    for key1,value1 in value.iteritems():
#        if value1>0.7:
#            if tag_dict[key1][key]<0.5:
#                print>>out, [key1,key]
            


