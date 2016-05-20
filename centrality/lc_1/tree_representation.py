from __future__ import division
import cjson
from collections import defaultdict,deque
from operator import itemgetter
import sys
from copy import deepcopy
import random
import Queue
class build_tree(object):
    def tree_from_gpd(self, gpd):
        in_out_dict=defaultdict(dict)
        for key,parent in gpd.iteritems():
            #print key
            parent=parent[0]
            if parent not in in_out_dict.keys():
                in_out_dict[parent]={"out":[],"in":[]}
            if key not in in_out_dict.keys():
                in_out_dict[key]={"out":[],"in":[]}
            in_out_dict[parent]["out"].append(key)
            in_out_dict[key]["in"].append(parent)
        return in_out_dict
    def merge_gpd(self, gpd_bb_old,gpd_lc):
        existingtag=[]
        gpd_bb=deepcopy(gpd_bb_old)
        print len(gpd_bb)        
        for key,value in gpd_lc.iteritems():
            if value[0]!='ROOT' and value[1]>0.3 and key in gpd_bb:
                if gpd_bb[key][0]=="ROOT":
                    gpd_bb[key]=gpd_lc[key]
            else:
                gpd_bb[key]=gpd_bb.get(key,gpd_lc[key])
        
        for key,value in gpd_bb.iteritems():
            if value[0]!='ROOT':
                existingtag.append(value[0])
        for tag in existingtag:
            if tag not in gpd_bb:
                #print tag
                gpd_bb[tag]=['ROOT',0]
        
        remove=[]
        for key,value in gpd_bb.iteritems():
            self.check_ring(key,value,gpd_bb,gpd_bb_old)
            if value[0]!='ROOT' and key==gpd_bb[value[0]][0]:
                #print 'rm-',key,value
                tmp=gpd_bb[value[0]]
                if value[1] !=int(value[1]):
                    remove.append(key)
                elif gpd_bb[value[0]][1]!=int(tmp[1]):
                    remove.append(value[0])
                else:
                    if value[1]>=tmp[1]:
                        remove.append(value[0]) 
                    else:
                        remove.append(key)
        infile=open('./bbf-v1-p')
        bbf=cjson.decode(infile.readline())
        for key in set(remove):
            print 'rr', key
            if gpd_bb[key][0]!= bbf[key][0][0]:
                gpd_bb[key]=bbf[key][0]
            else:
                gpd_bb[key]=bbf[key][1]
        #    self.check_ring()
        #    self.check_ring()
        #    del gpd_bb[key]        
        print len(gpd_bb)
        return gpd_bb

    def check_ring(self,key,value,gpd_bb,gpd_bb_old):
        exist=[]
        ances=[]
        tmp=key        
        while gpd_bb[tmp][0]!="ROOT":
            if tmp in exist:
                #need to cut the ring
                exist.append(tmp)
                #print exist
                for i in range(len(exist)):
                    #print len(exist),i,exist[i]
                    if exist[i]==tmp:
                        #print exist
                        exist=exist[i+1:]
                        if len(exist)>2:
                            print exist
                            for item in exist:
                                if item not in gpd_bb_old:
                                    gpd_bb[item]=['ROOT',0]
                        break
                    else:
                        pass
                return True
            else:
                exist.append(tmp)
                ances.append([tmp,gpd_bb[tmp][0],gpd_bb[tmp][1]])
                tmp=gpd_bb[tmp][0]
        return False
        #print exist
    
    def structural_eval(self,tree):
        lvl=[]
        length=[]
        tmplvl=["ROOT"]
        lvl.append(tmplvl)
        while tmplvl !=[]:
            new_lvl=[]
            for key in tmplvl:
                for item in tree[key]['out']:
                    new_lvl.append(item)
            tmplvl=new_lvl
            lvl.append(tmplvl)
        total_num=0    
        for lvs in lvl:
            length.append(len(lvs))
            total_num+=len(lvs)
        percenta=[]
        percenta=[t/total_num for t in length]
        aut=0
        for i in range(1,len(length)-1):
            aut+=(length[i]+length[i+1])*0.5
        cnt_b=0
        for item in lvl[1]:
            if tree[item]['out']==[]:
                cnt_b+=1
        #average depth
        print cnt_b
        total_num-=cnt_b
        length[1]-=cnt_b
        aut1=0
        for i in range(1,len(length)-1):
            aut1+=(length[i]+length[i+1]-2)*0.5
        percenta1=[t/total_num for t in length]
        return [percenta,percenta1,aut,aut1]
    def partial_folk(self,key,inoutdict):
        parent=[]
        child=[]
        sibling=[]
        if key in inoutdict:
            parent=inoutdict[key]["in"]
            if parent[0]=="ROOT":
                sibling=[]
            else:
                sibling=inoutdict[parent[0]]["out"]
            child=inoutdict[key]['out']
        return key,{"p":parent,"s":sibling,"c":child}
    
class Dist_distribution(object):
    
    pass

class TagNetwork(object):
    #def __init__(self):
        #self.queue = deque()
        #self.found = False
    def build_tag_network_cosine(self,cosine,threshold):  
        network=defaultdict(dict)
        tt=cosine.readline()
        cosine=cjson.decode(tt)
        for key,value in cosine.iteritems():
            if value>threshold:
                [key1,key2]=key.split('_')
                if key1 not in network:
                    network[key1]={"in":[key2],'out':[]}
                else:
                    network[key1]['in'].append(key2)
                if key2 not in network:
                    network[key2]={"in":[key1],'out':[]}
                else:
                    network[key2]["in"].append(key1)
        return network

    def build_tag_network_rulelist(self,rulelist,threshold):
        network=defaultdict(dict)
        for line in rulelist:
            line=cjson.decode(line)
            if line[-2]>=threshold:
                if line[0] not in network:
                    network[line[0]]={'in':[line[1]],'out':[]}
                else:
                    network[line[0]]['in'].append(line[1])
                if line[1] not in network:
                    network[line[1]]={'in':[line[0]],'out':[]}
                else:
                    network[line[1]]['out'].append(line[0])
        return network
    def shortest_path(self,network,node1,node2):
        nodes=network.keys()
        nodes_temp={}
        visited=[]
        for node in nodes:
            nodes_temp[node]=1000
        nodes_temp[node1]=0
        dist={}
        for node in nodes:
            dist[node]=1000
        dist[node1]=0
        while nodes_temp:
            #print nodes_temp
            u=sorted(nodes_temp.items(),key=itemgetter(1))[0][0]
            visited.append(u)
            dist[u]=nodes_temp[u]
            del nodes_temp[u]
            u_neighbour=network[u]['in']+network[u]['out']
            for item in u_neighbour:
                #if item=='yoga':
                #    print u
                if item not in visited:
                    alt=dist[u]+1
                    if alt<nodes_temp[item]:
                        nodes_temp[item]=alt
        print dist[node2],'N'
        return [node1,node2,dist[node2],'N']
   

    def bfs(self,network,node1,node2='nonono'):
        newnode=deque()
        newnode.append(node1)
        clique=[node1]
        while newnode:
            #self.queue.append(newnode)
            item=newnode.popleft()
            neighbour=network[item]["in"]+network[item]["out"]
            if neighbour==[]:
                continue
            else:
                for item in neighbour:
                    if item not in clique and item!='ROOT':
                        newnode.append(item)
                        clique.append(item)
        return clique
                

    def bfs_v1(self,network,node1,node2):
        distance={}
        distance[node1]=0
        visited=["ROOT"]
        queue=deque()
        queue.append(node1)
        found=False
        while found==False:  
            #print self.queue
            if not queue:
                print "not found"
                return node1,node2,1000,'not connected'
            
            dequestate=queue.popleft()
            visited.append(dequestate)
            new=network[dequestate]["in"]+network[dequestate]["out"]
            nextstate=[]
            for item in new:
                if item not in visited:
                    nextstate.append(item)
                    #print item,'item',dequestate,distance[dequestate]
                    distance[item]=distance[dequestate]+1
            for item in nextstate:
                if item != node2:
                    queue.append(item)
                else:
                    print "TRUE"
                    found=True
                    print distance[item]
        return [node1,node2,distance[node2],'T']

    def bfs_v2(self,network,node1,node2):
        found=False
        distance={}
        distance[node1]=0
        visited=['ROOT']
        queue=deque()
        queue.append(node1)
        while found==False:  
            #print len(self.queue)
            if not queue:
                print 'not connected'
                return node1,node2,1000,'not connected'
            dequestate=queue.popleft()
            visited.append(dequestate)
            par=network[dequestate]["in"][0]
            if par!='ROOT':
                new=set(network[dequestate]["in"]+network[dequestate]["out"]+network[par]["out"])
            else:
                new=set(network[dequestate]["in"]+network[dequestate]["out"])
            nextstate=[]
            for item in new:
                if item not in visited:
                    #if item==node2:
                        #print dequestate,item
                    nextstate.append(item)
                    distance[item]=distance[dequestate]+1
            for item in nextstate:
                if item != node2:
                    queue.append(item)
                else:
                    found=True
                    print distance[item],'T'
        return [node1,node2,distance[node2],'T']



    def connected_cpn(self,network,node1):
        nodes={}
        for node in network.keys():
            nodes[node]=0
        del nodes['ROOT']
        components=[]
        out1=open('te','w')
        while nodes:
            key=random.choice(nodes.keys())
            comp=self.bfs(network,key,'nonono')
            for tag in comp:
                del nodes[tag]
            components.append(comp)
            
            out1.write(cjson.encode(comp)+'\n')
        return components

class SearchSimulation(object):
    def node(self):
        pass
    def bfs(self, start, target):
        pass


def main1():
    infile1=open(sys.argv[1],'r')
    infile2=open(sys.argv[2],'r')
    gpd_bb=cjson.decode(infile1.readline())
    gpd_lc=cjson.decode(infile2.readline())
    tree=build_tree()
    newgpd=gpd_lc
    #newgpd=tree.merge_gpd(gpd_bb,gpd_lc)
    outfile=open(sys.argv[3],'w')
    #outfile.write(cjson.encode(newgpd))
    inoutdict=tree.tree_from_gpd(newgpd)
    strfile=open('./structure-conf','a')
    #strfile.write(cjson.encode(tree.structural_eval(inoutdict))+'\n')
    test=['nba','health','energy','texas','musician','california','google','startup', 'nfl', 'humor','rocket','gop','pet']
    for key in test:
        relations=tree.partial_folk(key,inoutdict)
        outfile.write(cjson.encode(relations)+'\n')

#----------------------------
    #infile=open(sys.argv[1],'r')
    #gpd=cjson.decode(infile1.readline())
    #tree.tree_from_gpd(gpd)

def main():
    infile1=open(sys.argv[1],'r') #gpd
    infile2=open(sys.argv[2],'r') #rulelist
    
    Eva=TagNetwork()
    network=Eva.build_tag_network_cosine(infile2,0.3)
    print network
    gpd=cjson.decode(infile1.readline())
    tree=build_tree()
    folkinoutdict=tree.tree_from_gpd(gpd)
    connected=Eva.connected_cpn(folkinoutdict,'sport')
    print len(connected)
    #for i in range(len(connected)):
    #    print 'wtf',len(connected[i])
    minlen=20
    maxlen=0
    index=0
    newc=[]
    for i in range(len(connected)):
         if len(connected[i])>minlen:
             newc.append(connected[i]) 
             print connected[i]

    #main=connected[index]
    #print len(main)
    out=open(sys.argv[3],'w')
    print>>out,"test"
    for i in range(1000):
        inx=random.randint(0,len(newc)-1)
        inx1=random.randint(0,len(newc[inx])-1)
        inx2=random.randint(0,len(newc[inx])-1)
        #print inx1,inx2
        if inx1!=inx2: 
            node1=newc[inx][inx1]
            node2=newc[inx][inx2]
            print node1,node2
    #out=open('tt','w')
    #for item,v in network.iteritems():
    #    print >>out,item,v
            d1=Eva.shortest_path(network,node1,node2)
            #print>>out, "start2"
            d2=Eva.bfs_v1(folkinoutdict,node1,node2)
            out.write(cjson.encode(d1)+'\n')
            out.write(cjson.encode(d2)+'\n')
if __name__=='__main__':
    main()
