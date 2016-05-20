from __future__ import division
import cjson
from collections import defaultdict
from operator import itemgetter
import sys
from copy import deepcopy

class build_tree(object):
    def tree_from_gpd(self, gpd):
        in_out_dict=defaultdict(dict)
        for key,parent in gpd.iteritems():
            parent=parent[0]
            if parent not in in_out_dict.keys():
                in_out_dict[parent]={"out":[],"in":[]}
            if key not in in_out_dict.keys():
                in_out_dict[key]={"out":[],"in":[]}
            in_out_dict[parent]["out"].append(key)
            in_out_dict[key]["in"].append(parent[0])
        return in_out_dict
    def merge_gpd(self, gpd_bb_old,gpd_lc):
        existingtag=[]
        gpd_bb=deepcopy(gpd_bb_old)
        print len(gpd_bb)        
        for key,value in gpd_lc.iteritems():
            #print key,value,gpd_bb[key]
            if value[0]!='ROOT' and value[1]>0.5 and key in gpd_bb:
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
            aut1+=(length[i]+length[i+1])*0.5
        percenta1=[t/total_num for t in length]
        return [percenta,percenta1,aut,aut1]

class Dist_distribution(object):
    
    pass

class TagNetwork(object):
    def build_tag_network(cosine):  
        pass 
class SearchSimu(object):
    def node(self):
        pass
    def bfs(self, start, target):
        pass


if __name__=='__main__':
    infile1=open(sys.argv[1],'r')
    infile2=open(sys.argv[2],'r')
    gpd_bb=cjson.decode(infile1.readline())
    gpd_lc=cjson.decode(infile2.readline())
    tree=build_tree()
    newgpd=tree.merge_gpd(gpd_bb,gpd_lc)
    outfile=open(sys.argv[3],'w')
    outfile.write(cjson.encode(newgpd))
    inoutdict=tree.tree_from_gpd(newgpd)
    print tree.structural_eval(inoutdict)
    
#----------------------------
    #infile=open(sys.argv[1],'r')
    #gpd=cjson.decode(infile1.readline())
    #tree.tree_from_gpd(gpd)
    
