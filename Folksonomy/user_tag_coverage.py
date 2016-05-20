import cjson
from operator import itemgetter
infile = '/spare/wei/user_tag_dict_sift_1'
userlist=[]
for line in open(infile,'r'):
    #line=line.split('\t')[1]
    line=cjson.decode(line)
    userlist.append(line)
aaa=sorted(userlist,key=itemgetter(2),reverse=1)
user_tag_coverage=[]
user_tag_cnt=[]
tags=[]
last_user_sum=0
for ls in aaa:
    user_tag_cnt.append([ls[0],len(ls[1])])
    num_new=0
    for key,value in ls[1].iteritems():

        if key not in tags:
            num_new+=1
            tags.append(key)
    user_tag_coverage.append([ls[0],num_new,num_new+last_user_sum])
    last_user_sum=num_new+last_user_sum    
outfile=open('/spare/wei/user_tag_coverage','w')
outfile.write(cjson.encode(user_tag_coverage)+'\n')
outfile.write(cjson.encode(user_tag_cnt)+'\n')

