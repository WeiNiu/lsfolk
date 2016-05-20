from __future__ import division
import cjson
import sys
#args tag_user_dict cosine
#infile='/spare/wei/tag_user_dict_l1'
infile=sys.argv[1]#'/spare/wei/local/tag_user_dict_ch3'
tag_list=[]
#useless=['and','the','my','of','for']
for line in open(infile,'r'):
    #line=line.split('\t')[1]
    line=cjson.decode(line)
    tag_list.append(line)
cosine_dict={}
centrality={}
for i in range(len(tag_list)):
    cur=tag_list[i]
    for j in range(i+1,len(tag_list)):
        com=tag_list[j]
        cosine=0
        for key,value in cur[1].iteritems():
            cosine+=value*com[1].get(key,0)
        if cosine>=0.1:
            cosine_dict[cur[0]+'_'+com[0]]=cosine
            centrality[cur[0]]=centrality.get(cur[0],0)+cosine
            centrality[com[0]]=centrality.get(com[0],0)+cosine
outfile=sys.argv[2]#'/spare/wei/local/cosine_ch3'
#outfile1='/spare/wei/noise_centrality_0.1_l1'
outfile=open(outfile,'w')
outfile.write(cjson.encode(cosine_dict))
#outfile1=open(outfile1,'w')
#outfile1.write(cjson.encode(centrality))
            

