import cjson
infile='/spare/wei/cosine'
outfile=open('/spare/wei/cosine_distribute','w')
interval1=0.01
invertal2=0.02

distribute1=[0 for i in range(101)]
distribute2=[0 for i in range(51)]
cosine=open(infile,'r')
cosine=cjson.decode(cosine.readline())
print len(cosine)
for key,value in cosine.iteritems():
    value1=int(value*100)
    value2=int(value*50)
    distribute1[value1]+=1
    distribute2[value2]+=1
outfile.write(cjson.encode(distribute1)+'\n')
outfile.write(cjson.encode(distribute2)+'\n')

