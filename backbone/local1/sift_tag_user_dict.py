import sys
import cjson
infilename=str(sys.argv[1])
outfilename=str(sys.argv[2])
unique=str(sys.argv[3])
uniquetag=open(unique,'w')
outfile=open(outfilename,'w')
infile=open(infilename,'r')
print infilename,outfilename
unique_tag={}
for line in infile:
#    print line
    line = line.split('\t')
    tagdict = cjson.decode(line[1])
    if len(tagdict[1])<5 or tagdict[-1]<5:
        continue
    else:
        unique_tag[tagdict[0]]=tagdict[-1]
        outfile.write(cjson.encode(tagdict)+'\n')
uniquetag.write(cjson.encode(unique_tag)+'\n')



