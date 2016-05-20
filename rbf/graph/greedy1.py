import cjson
from operator import itemgetter
from copy import deepcopy
from collections import defaultdict
from collections import deque
#edgedict{edge:[]}
#node:in:[] out:[]   bfs in this graph.
import sys
def construct_directed_graph_from_rules(rules_file,tagfreqdict):
    graph={}
    graph['ROOT']={'out':{},'in':{}}
    edges={}
    tagfreqdict=cjson.decode(tagfreqdict.readline())
    for tag in tagfreqdict:
        graph[tag]={'out':{},'in':{}}
    numnode=len(tagfreqdict)
    for rule in rules_file:
        rule = cjson.decode(rule)
        if rule[2]>0.3:
            graph[rule[0]]['in'][rule[1]]=rule[2]
            graph[rule[1]]['out'][rule[0]]=rule[2]
            edges[(rule[1],rule[0],rule[2])]=1
    for tag in tagfreqdict:
        if graph[tag]['in']=={}:
            graph['ROOT']['out'][tag]=0.1
            graph[tag]['in']['ROOT']=0.1
            edges[('ROOT',tag,0.1)]=1
    return graph,edges,numnode

def reduce_graph(graph,edges):
    for node in graph:
        if len(graph[node]['in'])<3:
            continue
        else:
            outlist=sorted(graph[node]['in'].items(),key=itemgetter(1))[:-3]
            for item,v1 in outlist:
                del graph[node]['in'][item]
                del graph[item]['out'][node]
                del edges[(item,node,v1)]
    return graph,edges

def bfs(graph,initial,goal):
    queue=deque()
    queue.append([initial])
    while queue:
        path=queue.popleft()
        node=path[-1]
        if node == goal:
           return len(path)-1,path
        temp=graph[node]['in'].keys()+graph[node]['out'].keys()
        print temp
        for key in temp:
            new_path = list(path)
            new_path.append(key)
            queue.append(new_path)


    #find the shortest path between the start and goal
def shortest(graph,initial,goal):
    dist={}
    prev={}
    vdict={}
    for key in graph:
        #print key
        vdict[key]=100
        dist[key]=100
        prev[key]=None
    dist[initial]=vdict[initial]=0
    while goal in vdict:
        u=sorted(vdict.items(),key=itemgetter(1))[0][0]
        #print u
        del vdict[u]
        temp=graph[u]['in'].keys()+graph[u]['out'].keys()
        for node in temp:
            if node in vdict:
                alt=dist[u]+1
                if alt < vdict[node]:
                    dist[node]=alt
                    vdict[node]=alt
                    prev[node]=u
    return dist[goal],prev[goal]

def shortest_weight(graph,initial,goal):
    dist={}
    prev={}
    vdict={}
    for key in graph:
        #print key
        vdict[key]=100
        dist[key]=100
        prev[key]=None
    dist[initial]=vdict[initial]=0
    while goal in vdict:
        u=sorted(vdict.items(),key=itemgetter(1))[0][0]
        #print graph[u]
        del vdict[u]
        #temp=graph[u]['in'].keys()+graph[u]['out'].keys()
        temp=deepcopy(graph[u]['in'])
        temp.update(graph[u]['out'])
        
       # print temp
        for node,value in temp.iteritems():
            if node in vdict:
                alt=dist[u]-value+1
                if alt < vdict[node]:
                    dist[node]=alt
                    vdict[node]=alt
                    prev[node]=[u,value]
                   # print node, u
    cur=goal
    trail=[]
    cost=1
    while cur != initial:
        trail.append(prev[cur][1])
        cost*=abs(prev[cur][1])
        cur=prev[cur][0]
    trail.append(cost)
    return dist[goal],trail

def build_gpd(graph,edges,numnode,loc):
    n=0
    while len(edges)>numnode:
        edgedict=[]
        print len(edges)
        nn=0
        for edge in edges:
            nn+=1
            print nn
            cur_graph=deepcopy(graph)
            if len(graph[edge[1]]['in'])>=2:
                del cur_graph[edge[0]]['out'][edge[1]]
                del cur_graph[edge[1]]['in'][edge[0]]
                print edge
                hops,trail=shortest(cur_graph,edge[0],edge[1])
                print hops,trail
                cost=(hops-1)*edge[2]**2
                #cost=abs(edge[2]-trail[-1])
                print 'cost',cost
                edgedict.append([edge[0],edge[1],edge[2],hops,cost])
        outfile1=open('edgedict2'+loc,'w')
        outfile1.write(cjson.encode(edgedict))
        #print edgedict
        rmls=sorted(edgedict,key=itemgetter(4))
        for rml in rmls:
            if len(edges)>numnode and len(graph[rml[1]]['in'])>=2:
        #print rml
                del graph[rml[0]]['out'][rml[1]]
                del graph[rml[1]]['in'][rml[0]]
                del edges[(rml[0],rml[1],rml[2])]
            else:
                pass
        #n+=1
        #print 'round',n
    gpd={}
    for edge in edges:
        gpd[edge[1]]=[edge[0],edge[2]]
    return gpd

def gpd_continue(edgelist,edges,graph,numnode):
    rmls=sorted(edgelist,key=itemgetter(4))
    for rml in rmls:
        if len(edges)>numnode and len(graph[rml[1]]['in'])>=2:
    #print rml
            del graph[rml[0]]['out'][rml[1]]
            del graph[rml[1]]['in'][rml[0]]
            del edges[(rml[0],rml[1],rml[2])]
        else:
            pass
        #n+=1
        #print 'round',n
    gpd={}
    for edge in edges:
        gpd[edge[1]]=[edge[0],edge[2]]
    return gpd



def main():
    rulefile=open(sys.argv[1],'r')
    tagfreqdict=open(sys.argv[2],'r')
    graph,edges,numnode=construct_directed_graph_from_rules(rulefile,tagfreqdict)
    graph,edges=reduce_graph(graph,edges)
    #outfile=open('test','w')
    #print>>outfile,graph
    #print>>outfile,edges
    gpd=build_gpd(graph,edges,numnode,sys.argv[3])
    outfile=open(sys.argv[4],'w')
    outfile.write(cjson.encode(gpd))

def mainxxx():
    rulefile=open('/Users/wei/Documents/folk_exp/centrality/lc/rulelist_tfidf_new_hou','r')
    tagfreqdict=open('/Users/wei/Documents/folk_exp/backbone/lc/tag_freq_dict_hou','r')
    graph,edges,numnode=construct_directed_graph_from_rules(rulefile,tagfreqdict)
    graph,edges=reduce_graph(graph,edges)
    #outfile=open('test','w')
    #print>>outfile,graph
    #print>>outfile,edges
    #gpd=build_gpd(graph,edges,numnode)
    edgelistfile=open('edgedict_hou','r')
    edgelist=cjson.decode(edgelistfile.readline())
    gpd=gpd_continue(edgelist,edges,graph,numnode)
    outfile=open('gpd_hou11','w')
    outfile.write(cjson.encode(gpd))

def costfunc():
    rulefile=open('/Users/wei/Documents/folk_exp/centrality/lc/rulelist_tfidf_new_hou','r')
    tagfreqdict=open('/Users/wei/Documents/folk_exp/backbone/lc/tag_freq_dict_hou','r')
    graph,edges,numnode=construct_directed_graph_from_rules(rulefile,tagfreqdict)
    graph,edges=reduce_graph(graph,edges)
    #outfile=open('test','w')
    #print>>outfile,graph
    #print>>outfile,edges
    #gpd=build_gpd(graph,edges,numnode)
    edgelistfile=open('edgedict_hou','r')
    edgelist=cjson.decode(edgelistfile.readline())

    for i in range(len(edgelist)):
        edgelist[i][-1]=(edgelist[i][2]**2)*(edgelist[i][3]-1)
    gpd=gpd_continue(edgelist,edges,graph,numnode)
    outfile=open('gpd_hou_cost','w')
    outfile.write(cjson.encode(gpd))


def test():
    rulefile=open('/Users/wei/Documents/folk_exp/centrality/lc/rulelist_tfidf_new_hou','r')
    tagfreqdict=open('/Users/wei/Documents/folk_exp/backbone/lc/tag_freq_dict_hou','r')
    graph,edges,numnode=construct_directed_graph_from_rules(rulefile,tagfreqdict)
    cur_graph=deepcopy(graph)
    if len(graph['texas ranger']['in'])>=2:
        del cur_graph['mlb']['out']['texas ranger']
        del cur_graph['texas ranger']['in']['mlb']
        #print edge
    print shortest(cur_graph,'mlb','texas ranger')
    pass
if __name__ == '__main__':
    main()
