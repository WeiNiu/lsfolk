import cjson
outfile='data8'
outfile=open(outfile,'w')
for line in open('data7','r'):
    line=line.split('\t')[1]
    #line=cjson.decode(line)
    #sumc=0
    #for key,value in line[1].iteritems():
    #    sumc+=value
    #line.append(sumc)
    outfile.write(line)

