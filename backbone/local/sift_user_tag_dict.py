#remove tag that are not in the tag_user_dict
import sys
import cjson
argv=sys.argv
#inputfilename unique_tag outputfilename
infile1=open(argv[1],'r')
infile2=open(argv[2],'r')
tag_f=cjson.decode(infile2.readline())
tag_f=tag_f.keys()
outfile=open(argv[3],'w')
for line in infile1:
    line=line.split('\t')[1]
    line=cjson.decode(line)
    dictt={}
    for key,value in line[1].iteritems():
        if key in tag_f:
            dictt[key]=value
    outfile.write(cjson.encode([line[0],dictt])+'\n')

