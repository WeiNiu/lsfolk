import cjson
stopwordfile='./stopword'
listt=[]
for line in open(stopwordfile,'r'):
    line=line.strip()
    if line not in listt:
        listt.append(line)
print listt
#print len(listt) 
outfile='./stopwordlist'
f=open(outfile,'w')
f.write(cjson.encode(listt))

