#get tag_freq_dict for training data from user_tag_dict
import sys
import cjson
infilename=str(sys.argv[1])
outfilename=str(sys.argv[2])
#unique=str(sys.argv[3])
#uniquetag=open(unique,'w')
outfile=open(outfilename,'w')
infile=open(infilename,'r')
print infilename,outfilename
#unique_tag={}
tag_freq_dict={}
for line in infile:
#    print line
    #line = line.split('\t')
    tagdict = cjson.decode(line)[1]
    for key,value in tagdict.iteritems():
        tag_freq_dict[key]=tag_freq_dict.get(key,0)+value
    #if len(tagdict[1])<5 or tagdict[-1]<9:
    #    continue
    #else:
        #unique_tag[tagdict[0]]=tagdict[-1]
outfile.write(cjson.encode(tag_freq_dict)+'\n')
#uniquetag.write(cjson.encode(unique_tag)+'\n')



