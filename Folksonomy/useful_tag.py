import cjson
from operator import itemgetter
from collections import defaultdict
#parent_child_dict
infile1='/spare/wei/local/p_c_dict_ch3'
infile1=open(infile1,'r')
pc_dict=cjson.decode(infile1.readline())
#cosine
infile2='/spare/wei/local/cosine_ch31'

#selected user_tag_dict
infile3='/spare/wei/local/user_tag_dict_ch3'
outfile=open('newtag_folk_confidence','w')
infile2=open(infile2,'r')
cosinedict=cjson.decode(infile2.readline())

#infile3=open(infile3,'r')
cnt=0

for line in open(infile3,'r'):
    cnt+=1
    if cnt>10:
        break
    centrality={}
    closest=defaultdict(list)
    tags = cjson.decode(line)[1]
    for tag,value in tags.iteritems():
        for tag1,value1 in tags.iteritems():
            if tag !=tag1:
                sim=cosinedict.get(tag+'_'+tag1,0)+cosinedict.get(tag1+'_'+tag,0)
                if sim>0.75:#same thing
                    sim=0
                centrality[tag]=centrality.get(tag,0)+sim
                if tag not in closest.keys():
                    closest[tag]=[value,tag1,sim,value*sim]
                else:
                    if sim>closest[tag][2]  and tag not in tag1 and tag1 not in tag:
                        
                        closest[tag]=[value,tag1,sim,value*sim]
    currenttag=closest.keys()
    centrality1=sorted(centrality.items(), key=itemgetter(1),reverse=1)#seems not good
    closest1=sorted(closest.items(), key=itemgetter(1),reverse=1)#able to use, raw cnt+dist
    closest2=sorted(closest.items(), key=lambda e: e[1][2],reverse=1)#distance to closest neighbour tag
    closest3=sorted(closest.items(), key=lambda e: e[1][3],reverse=1)
    print line
    print>>outfile,currenttag
    #print centrality1
    #print closest1
    #print closest2
    #print>>outfile, closest3
    print'----------'
    new_tag=[]
    length=len(closest3)
    for tag,value in closest3[:int(length/10)]:
        if tag not in pc_dict.keys():
            continue
        parent=pc_dict[tag]['parent']
        if parent not in currenttag and parent!='a':
            new_tag.append(parent)
        child=pc_dict[tag]['child']
        if child !=[] and child not in currenttag:
            for item in child:
                new_tag.append(item)
    print>>outfile, 'new_tag',new_tag
