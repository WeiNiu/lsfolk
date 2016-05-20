import cjson
from operator import itemgetter
from collections import defaultdict
import networkx as nx


def build_tree(nodes):
    # create empty tree to fill
    tree = {}

    # fill in tree starting with roots (those with no parent)
    build_tree_recursive(tree, 'ROOT', nodes)
    return tree

def build_tree_recursive(tree, parent, nodes):
    # find children
    children  = [n for n in nodes.keys() if nodes[n] == parent]

    # build a subtree for each child
    for child in children:
    # start new subtree
        tree[child] = {}
    # call recursively to build a subtree for current node
        build_tree_recursive(tree[child], child, nodes)

def print_dict(dictionary,outfile,ident = '', braces=1):

    """ Recursively prints nested dictionaries."""
    
    for key, value in dictionary.iteritems():
        if isinstance(value, dict):
            outfile.write(  '%s%s\n' %(ident,key) )
            print_dict(value, outfile, ident+'  ')
        else:
            outfile.write(ident+'%s = %s\n' %(key, value))
#infile='/spare/wei/folk/cosine_dict_sf_u3_5'
#infile='/spare/wei/folk/cosine_dict_dallas'
infile='/spare/wei/local/cosine_ch3'
infile=open(infile,'r')
cosine_dict=cjson.decode(infile.readline())


centrality_list=[]
for key,value in cosine_dict.iteritems():
    centrality=0
    for tag,freq in value.iteritems():
        centrality+=freq
    centrality_list.append([key,centrality])
a=sorted(centrality_list,key=itemgetter(1),reverse=1)
outfile1=open('centrality_chicago','w')
for tag,cen in a:
    outfile1.write(cjson.encode([tag,cen])+'\n')

#algorithm
THRESHOLD=0.3
graph_parent_dict={}
G=nx.DiGraph()
#G.add_node('root')
#for tag,centrality in centrality_list:
b=a
for tag,cen in b:
    max_can_value=0
    max_can=''
    for node in G.nodes():
        similarity=cosine_dict[node].get(tag,0)
        if similarity>max_can_value:
            max_can_value=similarity
            max_can=node
    if max_can_value>THRESHOLD:
        G.add_node(tag)
        G.add_edge(max_can,tag)
        #print 'new tag',tag
        #print 'root',max_can
        #print graph_dict
        #graph_dict[str(max_can)][tag]={}
        graph_parent_dict[tag]=max_can
    else:
        G.add_node(tag)
        graph_parent_dict[tag]='ROOT'

nx.write_gml(G,"clo_folksonomy_chicago_0.3.gml")
print graph_parent_dict
a= build_tree(graph_parent_dict)
print a
outfile2=open('clo_folksonomy_chicago_0.3','w')
print_dict(a,outfile2)
outfile3='clo_graph_parent_dict_chicago_0.3'
outfile3=open(outfile3,'w')
outfile3.write(cjson.encode(graph_parent_dict))
