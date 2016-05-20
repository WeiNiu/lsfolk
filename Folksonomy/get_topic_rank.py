import cjson
from operator import itemgetter
infilename='/spare/wei/folk/topic_rank_nonsingular_500'
rank_dict={}
for line in open(infilename,'r'):
    line=cjson.decode(line)
    rank_dict[line[0]]=line[1]
sorted_rank=sorted(rank_dict.iteritems(),key=itemgetter(1),reverse=1)
reduced=[]
for a,b in sorted_rank:
    if b>=50:
        reduced.append([a,b])
    else:
        break
outfile='./topic_rank_nonsigular_500_frequent'
o=open(outfile,'w')
for t in reduced:
    o.write(cjson.encode(t)+'\n')
print len(reduced)
