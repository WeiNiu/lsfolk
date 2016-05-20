#for centrality + conditional P 
import cjson
from operator import itemgetter
from collections import defaultdict
import networkx as nx
import sys

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
infile2=sys.argv[2]
infile2=open(infile2,'r')
removelist=cjson.decode(infile2.readline())
infile=sys.argv[1]
infile1=sys.argv[3]
cosine=open(infile1,'r')
cosine=cjson.decode(cosine.readline())
infile=open(infile,'r')
centrality_list=[]
for line in infile:
    line=cjson.decode(line)#infile.readline())
    centrality_list.append(line)
#centrality_list=[]
#for key,value in cosine_dict.iteritems():
#    centrality=0
#    for tag,freq in value.iteritems():
#        centrality+=freq
#    centrality_list.append([key,centrality])
a=sorted(centrality_list,key=itemgetter(1),reverse=1)
print a[1]
#outfile1=open('centrality','w')
#for tag,cen in a:
#    outfile1.write(cjson.encode([tag,cen])+'\n')

#algorithm
THRESHOLD=0.3
graph_parent_dict={}
graph_parent_dict_s={}
G=nx.DiGraph()
#G.add_node('root')
#for tag,centrality in centrality_list:

for tag,cen in a:
    if tag in removelist:
        continue
    max_can_value=0
    max_can=''
    for node in G.nodes():
        key1,key2=tag+'_'+node,node+'_'+tag
        b=cosine.get(key1,0)
        #c=cosine.get(key2,0)
        similarity=b
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
        graph_parent_dict_s[tag]=max_can
        graph_parent_dict[tag]=[max_can,max_can_value]
    else:
        G.add_node(tag)
        graph_parent_dict[tag]=['ROOT',0]
        graph_parent_dict_s[tag]='ROOT'

unique_file=open(sys.argv[6],'r')
taglist=cjson.decode(unique_file.readline())
taglist=taglist.keys()
print len(taglist),len(removelist)
for tag in taglist:
    if tag not in graph_parent_dict_s and tag not in removelist:
        graph_parent_dict_s[tag]="ROOT"
        graph_parent_dict[tag]=['ROOT',0]
#nx.write_gml(G,"noise_folksonomy_chi_025-1.gml")
#print graph_parent_dict
a= build_tree(graph_parent_dict_s)
#print a
outfile2=open(sys.argv[4],'w')
print_dict(a,outfile2)
outfile3=sys.argv[5]
outfile3=open(outfile3,'w')
outfile3.write(cjson.encode(graph_parent_dict))
