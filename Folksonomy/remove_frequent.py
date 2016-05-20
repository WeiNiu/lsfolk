import cjson

tagfreqdict={}
infile='/spare/wei/local/user_tag_dict_ch3'
ur_cnt=0
for line in open(infile):
    ur_cnt+=1
    line=cjson.decode(line)
    for key,value in line[1].iteritems():
        tagfreqdict[key]=tagfreqdict.get(key,0)+1
se=[]
for key,value in tagfreqdict.iteritems():
    if value>ur_cnt*.15:
        se.append(key)
        #print ur_cnt
        print key,value
print se
