#converting key from user to tags
from __future__ import division
import cjson
from collections import defaultdict
#filename='/spare/wei/folk/user_tag_dict_nonsingular_100_10'
filename='/user_tag_dict_l1'#'/spare/wei/folk/user_tag_dict_en_lt10_for_prob_1_3'#'/spare/wei/folk/user_tag_dict_en_for_prob'#user_tag_dict_greater_than_3000'
#filename='/spare/wei/folk/user_tag_dict_ny_u5_10'
outfile='/spare/wei/links'
out=open(outfile,'w')
outfile1='/spare/wei/tag-tag-dict_l1'#'./link-dict_en_lt10_3'
#outfile1='./link-dict_ny_u5_10'
out1=open(outfile1,'w')
tag_dict=defaultdict(dict)
for line in open(filename):
    tagdict = cjson.decode(line)[1]
    for tag,value in tagdict.iteritems():
        for tag1,value1 in tagdict.iteritems():
#            if tag == tag1:
            tag_dict[tag][tag1]=1+tag_dict[tag].get(tag1,0)
#            else:
#                tag_dict[tag][tag1]=1+tag_dict[tag].get(tag1,0)
#                tag_dict[tag1][tag]=1+tag_dict[tag1].get(tag,0)
out1.write(cjson.encode(tag_dict))                
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
            


