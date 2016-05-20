import cjson
from operator import itemgetter
infile = '/spare/wei/tag_user_dict_sift'
taglist=[]
for line in open(infile,'r'):
    line=cjson.decode(line)
    taglist.append(line)
aaa=sorted(taglist,key=itemgetter(2),reverse=1)
tag_user_coverage=[]
tag_user_cnt=[]
users=[]
last_tag_sum=0
for ls in aaa:
    tag_user_cnt.append([ls[0],len(ls[1])])
    num_new=0
    for key,value in ls[1].iteritems():
        if key not in users:
            num_new+=1
            users.append(key)
    tag_user_coverage.append([ls[0],num_new,num_new+last_tag_sum])
    last_tag_sum=num_new+last_tag_sum    
outfile=open('/spare/wei/tag_user_coverage','w')
outfile.write(cjson.encode(tag_user_coverage)+'\n')
outfile.write(cjson.encode(tag_user_cnt)+'\n')

