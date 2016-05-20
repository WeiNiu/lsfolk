import cjson
import networkx as nx
from operator import itemgetter
infile = '/spare/wei/folk/tag_cooccurence_less_than_50_en'
cooccur_dict={}
centrality=[]
for line in open (infile, 'r'):
    line=cjson.decode(line)
    cooccur_dict[line[0]]=line[1]
    c_sum=0
    for key, value in line[1].iteritems():
        c_sum+=value
    centrality.append([line[0],c_sum])
a=sorted(centrality,key=itemgetter(1),reverse=1)
outfile1 = './co_occur_centrality_sequence_50_en'
outfile1=open(outfile1,'w')
for tag,cen in a:
    outfile1.write(cjson.encode([tag,cen])+'\n')

#algorithm
THRESHOLD=2

G=nx.DiGraph()
#G.add_node('root')
#for tag,centrality in centrality_list:
b=a
for tag,cen in b:
    max_can_value=0
    max_can=''
    for node in G.nodes():
        similarity=cooccur_dict[node].get(tag,0)
        if similarity>max_can_value:
            max_can_value=similarity
            max_can=node
    if max_can_value>THRESHOLD:
        G.add_node(tag)
        G.add_edge(max_can,tag)
    else:
        G.add_node(tag)
nx.write_gml(G,"folksonomy_en_50_co_2.gml")
