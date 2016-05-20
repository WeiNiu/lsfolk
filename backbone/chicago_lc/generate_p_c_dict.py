#generating parent child dictionary like{food:{parent:media,child:[......]}} from 
#graph_parent_dict

import cjson
local='/spare/wei/local/%s'
infile=local%'graph_parent_dict_ch3-log1'
infile=open(infile,'r')
graph_parent_dict=cjson.decode(infile.readline())
p_c_dict={}
for key,value in graph_parent_dict.iteritems():
    if key not in p_c_dict.keys():
        p_c_dict[key]= {'parent':value, 'child':[]}
    else:
        p_c_dict[key]['parent']=value
    if value not in p_c_dict.keys():
        p_c_dict[value]={'parent':'a', 'child':[key]}
    else:
        p_c_dict[value]['child'].append(key)
outfile=open(local%'p_c_dict_ch3','w')
outfile.write(cjson.encode(p_c_dict))

