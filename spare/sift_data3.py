import cjson
infile='data5'
infile1='./uni_tag'
#taglist=[]
outfile=open('data6','w')
#for line in open(infile1,'r'):
#    taglist.append(line.split('\n')[0])
f=open(infile1,'r')
taglist=cjson.decode(f.readline())
tagset=set(taglist)
print tagset
for line in open(infile,'r'):
    line=cjson.decode(line)
    if line['tag'][0] in tagset:
        outfile.write(cjson.encode(line)+'\n')
    else:
        pass
