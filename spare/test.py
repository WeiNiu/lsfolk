import re
import nltk
import cjson
f='./list_peers.json'
for line in open(f,'r'):
    line=cjson.decode(line[12:])
    #print line.keys()
    title=line['list_name']
    titleSplit=re.split(r'\W+',title)
    if len(titleSplit)>1:
        print titleSplit
    #porter=nltk.stem.porter.PorterStemmer()
    #c=porter.stem_word(titleSplit[0])
    #print c
