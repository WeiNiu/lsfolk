import cjson
from nltk import PorterStemmer
infile='./stop_word_list_new'
x=PorterStemmer()
f=open(infile,'r')
listt=cjson.decode(f.readline())
nw=list(set(listt))
new_list=[]
for word in nw:
    word1=x.stem_word(word)
    if word1 not in new_list:
        new_list.append(word1)
newlist=list(set(new_list))
print new_list
print len(new_list)

outfile='./stop_word_porter_stems'
o=open(outfile,'w')
o.write(cjson.encode(new_list))
outfile1='./stop_word_list_new'
o1=open(outfile1,'w')
o1.write(cjson.encode(nw))
