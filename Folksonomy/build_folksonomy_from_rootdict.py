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
#G=nx.DiGraph()
#G.add_node('ROOT')
taglist=[]
infile1='/spare/wei/local/uni_tag_ch3'
#infile1='./link-dict_lt10'
infile1=open(infile1,'r')
taglist=cjson.decode(infile1.readline())


infile='/spare/wei/root_dict_en_0.1_l1-3'
infile='/spare/wei/local/root_dict_ch3-log'
#infile='/spare/wei/root_dict_en_log_0.1_v2'
#infile='root_dict_lt10_schz_0.6'
infile=open(infile,'r')
graph_parent_dict={}
for line in infile:
    root_dict=cjson.decode(line)
#    if root_dict[0] not in G.nodes():
#        G.add_node(root_dict[0])
#    if root_dict[1][0][0] not in G.nodes():
#        G.add_node(root_dict[1][0][0])
#    G.add_edge(root_dict[1][0][0],root_dict[0])
#for node in G.nodes():
#    if G.in_edges(node)==[] or G.in_edges(node)==None:
#        G.add_edge('ROOT',node)
    if root_dict[0][-4:]!=' and' and root_dict[1][0][1]>0.25:
        print root_dict[0][-4:],root_dict[0]
        graph_parent_dict[root_dict[0]]=root_dict[1][0][0]
    else:graph_parent_dict[root_dict[0]]='ROOT'
for tag in taglist:
    if tag not in graph_parent_dict.keys() and tag[-4:]!=' and' and tag[-3:]!='of':
        graph_parent_dict[tag]='ROOT'

#nx.write_gml(G,"folksonomy_en_rule.gml")
print graph_parent_dict
graph_p_d='/spare/wei/local/graph_parent_dict_ch3-log1'
outfile3=open(graph_p_d,'w')
outfile3.write(cjson.encode(graph_parent_dict))

a= build_tree(graph_parent_dict)
print a
outfile2=open('/spare/wei/local/folksonomy_ch3-log1','w')
print_dict(a,outfile2)
