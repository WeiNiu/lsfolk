import cjson 
infile1='graph_parent_dict_sf_cen_degree_0.2_0.3'
infile2='graph_parent_dict_ny_cen_degree_0.2_0.3'
infile1=open(infile1,'r')
infile2=open(infile2,'r')
outfile='123'
outfile=open(outfile,'w')
dict1=cjson.decode(infile1.readline())
dict2=cjson.decode(infile2.readline())
len1=len(dict1)
len2=len(dict2)
print len1,len2
cnt_same=0
cnt=0
for key,value in dict1.iteritems():
    if key in dict2.keys():
        cnt+=1
        if value==dict2[key]:
            cnt_same+=1
            #print key,value
        else:
            pass
            print>>outfile, key, dict1[key],dict2[key]
    #else: print key,value
print cnt,cnt_same
            
            
