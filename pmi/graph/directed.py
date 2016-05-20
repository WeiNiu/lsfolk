import cjson
from collections import defaultdict
import sys

def construct_directed_graph_from_rules(rules_file,tagfreqdict):
    graph=defaultdict(dict)
    tagfreqdict=cjson.decode(tagfreqdict.readline())
    for rule in rules_file:
        rule = cjson.decode(rule)
        if rule[2]>0.3:
        	graph[rule[1]][rule[0]]=-rule[2]
    for tag in tagfreqdict:
        graph['ROOT'][tag]=-0.1
    return graph

def _reverse(graph):
    r = {}
    for src in graph:
        for dst,c in graph[src].items():
            if dst in r:
                r[dst][src] = c
            else:
                r[dst] = { src : c }
    return r

def _getCycle(n,g,visited=set(),cycle=[]):
    visited.add(n)
    cycle += [n]
    if n not in g:
        return cycle
    for e in g[n]:
        if e not in visited:
            cycle = _getCycle(e,g,visited,cycle)
    return cycle


def _mergeCycles(cycle,G,RG,g,rg):
    allInEdges = []
    minInternal = None
    minInternalWeight = sys.maxint

    # find minimal internal edge weight
    for n in cycle:
        for e in RG[n]:
            if e in cycle:
                if minInternal is None or RG[n][e] < minInternalWeight:
                    minInternal = (n,e)
                    minInternalWeight = RG[n][e]
                    continue
            else:
                allInEdges.append((n,e))        

    # find the incoming edge with minimum modified cost
    minExternal = None
    minModifiedWeight = 0
    for s,t in allInEdges:
        u,v = rg[s].popitem()
        rg[s][u] = v
        w = RG[s][t] - (v - minInternalWeight)
        if minExternal is None or minModifiedWeight > w:
            minExternal = (s,t)
            minModifiedWeight = w

    u,w = rg[minExternal[0]].popitem()
    rem = (minExternal[0],u)
    rg[minExternal[0]].clear()
    if minExternal[1] in rg:
        rg[minExternal[1]][minExternal[0]] = w
    else:
        rg[minExternal[1]] = { minExternal[0] : w }
    if rem[1] in g:
        if rem[0] in g[rem[1]]:
            del g[rem[1]][rem[0]]
    if minExternal[1] in g:
        g[minExternal[1]][minExternal[0]] = w
    else:
        g[minExternal[1]] = { minExternal[0] : w }

def edmonds(root,G):
    RG = _reverse(G)
    if root in RG:
        RG[root] = {}
    g = {}
    for n in RG:
        if len(RG[n]) == 0:
            continue
        minimum = sys.maxint
        s,d = None,None
        for e in RG[n]:
            if RG[n][e] < minimum:
                minimum = RG[n][e]
                s,d = n,e
        if d in g:
            g[d][s] = RG[s][d]
        else:
            g[d] = { s : RG[s][d] }
            
    cycles = []
    visited = set()
    for n in g:
        if n not in visited:
            cycle = _getCycle(n,g,visited)
            cycles.append(cycle)

    rg = _reverse(g)
    for cycle in cycles:
        if root in cycle:
            continue
        _mergeCycles(cycle, G, RG, g, rg)

    return g



if __name__ == "__main__":
    try:
        filename = '../../centrality/lc/rulelist_tfidf1-hou'#sys.argv[1]
        rules_file=open(filename,'r')
        tagfreqdict=open('../lc/tag_freq_dict_hou','r')

        root = 'ROOT' #sys.argv[2]
    except IndexError:
        sys.stderr.write('no input and/or root node specified\n')
        sys.stderr.write('usage: python edmonds.py <file> <root>\n')
        sys.exit(1)
    G=construct_directed_graph_from_rules(rules_file,tagfreqdict)   
    h = edmonds(root,G)
    outfile=open('test','w')
    rootdict={}
    for s in h:
        for t in h[s]:
            rootdict[t]=s
            print>>outfile, "%s-%s" % (s,t)
    infile1=open('../../centrality/lc/gpd_hou','r')
    rootdict1=cjson.decode(infile1.readline())
    for key,value in rootdict1.iteritems():
        if rootdict[key]!=value[0]:
            print key,value, rootdict[key]
    


