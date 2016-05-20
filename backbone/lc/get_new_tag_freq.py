#composing a weighted version of confidence that has a unique denominator tag frequency.
import cjson
import sys
from collections import defaultdict
infile='./user_tag_dict_lcchi1'
infile1='./tag_user_dict_lcchi1'
taglist=[]
for line in open(infile1,'r'):
    line=cjson.decode(line)
    taglist.append(line[0])

tag_tag_cnt=defaultdict(dict)
for line in open(infile,'r'):
    line = cjson.decode(line)[1]
    for tag in taglist:
        if tag not in line:
            for key in line:
                if line[key]>=1:
                    tag_tag_cnt[tag][key]=tag_tag_cnt[tag].get(key,0)+1
                else:
                    tag_tag_cnt[tag][key]=tag_tag_cnt[tag].get(key,0)+line[key]
        elif tag in line:
            for key in line:
                tag_tag_cnt[tag][key]=tag_tag_cnt[tag].get(key,0)+min(line[tag],line[key])
outfile=open('cnt_new','w')
outfile.write(cjson.encode(tag_tag_cnt))
