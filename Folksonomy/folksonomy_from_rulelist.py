#look at code on local.
import networkx as nx
import cjson
infile='./rulelist'
G=nx.Graph()
for line in open(infile):
    line=cjson.decode(line)
    if line[0] == 'sports'or line[0]=='sport':
        if line[1] not in G.nodes():
            G.add_node(line[1])
            G.add_edge(line[0],line[1])
nx.write_gml(G,'sports.gml')
