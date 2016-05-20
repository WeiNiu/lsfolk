#remove trash tags.
#return max freq tag and freq
import cjson
infile='../data6'
#infile1='./user_tag_dict_mr'

tagf=0
tag_freq_dict={}
#user_tag_dict={}
mosttag=''
#aaa=[' and', 'and ','the ',' the', 'all ']
useless=['who','what','that','is','are','listing','listed','follower','follow','followed','tweep','i','list','you','from','in','on','to','and','the','for','all','my','of','your','s']
frequent=['list','peep', 'love', 'world', 'writer', 'stuff','web', 'social medium', 'info', 'blogger', 'interesting', 'tweep', 'social', 'medium', 'cool', 'peep', 'blog', 'folk']
outfile1=open('../data5','w')
for line in open(infile,'r'):
    #line=line.split('\t')[1]
    line=cjson.decode(line)
    split=line['tag'][0].split(' ')
#    print split
    flag=0
    if line['tag'] in frequent:
        print line['tag']
        flag=1
    for key in split:
        if key in useless:
            flag=1  
    if flag==0:#remove low freq tags
        #tag_freq_dict[line[0]]=line[2]
        #if line[2]>tagf:
        #    tagf=line[2]
        #    mosttag=line[0]
        outfile1.write(cjson.encode(line)+'\n')
#        tag=line[0]
#        tagf=line[-1]
#print mosttag,tagf
#outfile='/spare/wei/local/tag_freq_dict_ch3'
#outfile='/spare/wei/local/uni_tag_ch3'
#outfile=open(outfile,'w')
#outfile.write(cjson.encode(list(tag_freq_dict.keys())))

#for line in open(infile1,'r'):
#    line=line.split('\t')[1]
#    line=cjson.decode(line)
#    user_tag_dict[str(line[0])]=line[1]
#outfile='/spare/wei/user_tag_dict'
#outfile=open(outfile,'w')
#outfile.write(cjson.encode(user_tag_dict))

