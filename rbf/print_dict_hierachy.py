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
infile='./graph/gpd2_ny'
infile=open(infile,'r')
infile=cjson.decode(infile.readline())
dict1={}
for key,value in infile.iteritems():
    dict1[key]=value[0]
outfile='folk-c-ny'
outfile=open(outfile,'w')
a=build_tree(dict1)
print_dict(a,outfile)
