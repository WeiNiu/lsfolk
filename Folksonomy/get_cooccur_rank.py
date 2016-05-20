import cjson
from operator import itemgetter
infilename='/spare/wei/folk/tag_cooccurence_nonsingular_100'
rank_dict={}
for line in open(infilename,'r'):
    line=cjson.decode(line)
    rank_dict[line[0]]=line[1]
sorted_rank=sorted(rank_dict.iteritems(),key=itemgetter(1),reverse=1)
reduced=[]
for a,b in sorted_rank:
    if b>=1:
        reduced.append([a,b])
    else:
        break
outfile='./tag_cooccur_rank_1'
o=open(outfile,'w')
for k in reduced:
    o.write(cjson.encode(k)+'\n')
print len(reduced)
