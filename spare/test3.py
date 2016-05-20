import cjson
sift='tag_user_dict_sift_1'
f=open(sift,'w')
i=0

for line in open('tag_user_dict_sift','r'):
#    if i<22414:
#        i+=1
#        continue
   #line=cjson.decode(line)
    #line=line.split('\t')[1]
    line=cjson.decode(line)
    if line[0][-2:-1]!='of'  and line[0][-3:-1]!='and':
        f.write(cjson.encode(line)+'\n')
    else:
        pass
    #print line
    #line=cjson.decode(line)
    #f.write(line+'\n')
    
