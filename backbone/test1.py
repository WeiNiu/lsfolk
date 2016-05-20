from random import randint,shuffle
import itertools
line=[0,{"motivation": 1, "cool person": 1, "leader": 1, "networking": 1, "network": 5, "usa": 1, "author":1, "public": 1, "networker": 2, "network marketing": 4, "speaker": 2, "marketing": 8, "self development": 1, "cool": 1, "marketer": 1, "public speaker": 1, "network marketer": 1, "development": 1, "big name": 1, "business": 3, "marketing sale"    : 1, "successful": 1, "big": 1, "training": 1, "world": 1, "grow": 1, "inspiration": 1, "great": 1, "entrepreneur": 1, "guru": 1, "sale": 2, "us": 1, "mlm": 12, "connection": 1, "professional": 1, "vision": 1}]
nfold=4
tagdict=[{} for i in range(nfold)]
n=len(line[1])/nfold
fn=n*nfold
itera=0
randlist=[i for i in range(len(line[1]))]
shuffle(randlist)
taglist=[]
for key,value in line[1].iteritems():
    taglist.append([key,value])
for inx in randlist:
    num=0
    if num<fn:
        index=itera%nfold
        key=taglist[inx][0]
        value=taglist[inx][1]
        if key=='network maimport itertoolsrketer':
        	print index
        tagdict[index][key]=value
        itera+=1
    else:
        index=randint(0,nfold-1)
        tagdict[index][key]=value

for i in range(4):
	print tagdict[i],len(tagdict[i])
print len(line[1])
a=[14063553, {"motivation": 1, "cool person": 1, "leader": 1, "networking": 1, "network": 5, "usa": 1, "author": 1, "networker": 2, "network marketing": 4, "speaker": 2, "marketing": 8, "inspiration": 1, "public": 1, "development": 1, "business":     3, "big": 1, "training": 1, "world": 1, "cool": 1, "great": 1, "entrepreneur": 1, "guru": 1, "sale": 2, "us": 1, "mlm": 12, "marketer": 1, "connection": 1, "professional": 1}]
print len(a[1])