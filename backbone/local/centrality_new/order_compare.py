import cjson
from operator import itemgetter
infile1='/spare/wei/cosine_centrality'
infile2='/spare/wei/tag_user_dict_sift'

doc1 = open(infile1, 'r')
cosine=cjson.decode(doc1.readline())
cosine1=sorted(cosine.items(),key=itemgetter(1),reverse=1)
print cosine1[:50]
freqdict={}
for line in open(infile2,'r'):
    line=cjson.decode(line)
    freqdict[line[0]]=line[-1]
freqdict=sorted(freqdict.items(),key=itemgetter(1),reverse=1)
print freqdict[:50]
for i in range(50):
    print freqdict[i][0],cosine[freqdict[i][0]]
