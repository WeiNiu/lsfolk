from __future__ import division
import cjson
infile='/spare/wei/local/uni_tag_ch3'
#infile1='./ss_0.1_graph_parent_dict_0.1'
#infile1='./clo_graph_parent_dict_0.3'
infile1='/spare/wei/local/graph_parent_dict_ch3'
infile2='/home/wei/Folksonomy/centrality/noise_graph_parent_dict_chicago_0.4_02'

#infile2='./noise_graph_parent_dict_ch_025-1'
unitag=open(infile,'r')
unitag=cjson.decode(unitag.readline())
dict1=open(infile1,'r')
dict2=open(infile2,'r')
dict1=cjson.decode(dict1.readline())
dict2=cjson.decode(dict2.readline())
length=len(unitag)
cnt=0
ff=open('./ss_l1_l3','w')
for tag in unitag:
    f1=dict1.get(tag,'ROOT')
    f2=dict2.get(tag,'ROOT')
    if f1==f2:
        cnt+=1
    else:
        print>>ff, tag,'--', f1,'--',f2
print cnt/length, 'new:rule'
