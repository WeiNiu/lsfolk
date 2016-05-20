#remove tag with less than 100 freq and remove trival 'and'
import cjson
sift='tag_user_dict_sift'
f=open(sift,'w')
i=0
tag_dict='data4'
taglist=[]
for line in open(tag_dict,'r'):
    taglist.append(line.split('\n')[0])
tagset=set(taglist)
print tagset
for line in open('tag_user_dict_mr1','r'):
#    if i<22414:
#        i+=1
#        continue
   #line=cjson.decode(line)
    line=line.split('\t')[1]
    line=cjson.decode(line)
    if line[0] in tagset and line[-1]>100 and line[0][-3:-1]!='and' and line[0][0:3]!='and':
        f.write(cjson.encode(line)+'\n')
    else:
        pass
    #print line
    #line=cjson.decode(line)
    #f.write(line+'\n')
    
