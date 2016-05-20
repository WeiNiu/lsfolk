from __future__ import division
import cjson
infile1='./rulelist_2_0.3houston'
infile2='/Users/wei/Documents/folk_exp/backbone1/rulelist3_houston'
out=open('LL_GG_h','w')
rule_lc={}
rule_g={}
for line in open(infile1,'r'):
    line=cjson.decode(line)
    if line[2]>0.3:
        key=line[0]+'_'+line[1]
        rule_lc[key]=line[2]
for line in open(infile2,'r'):
    line=cjson.decode(line)
    if line[2]>0.3:
        key=line[0]+'_'+line[1]
        rule_g[key]=line[2]
cnt=0
sum1=0
cnt1=0
sum2=0
for key,value in rule_lc.iteritems():
    vv=rule_g.get(key,0)
    if vv!=0 and vv<value and value-vv>0.05:
        print>>out,key,'LL',value,vv
        cnt+=1
        sum1+=value
    elif vv!=0 and vv>value and vv-value>0.05:
        print>>out,key,'GG',value,vv
        cnt1+=1
        sum2+=vv
print cnt,cnt1,sum1/cnt,sum2/cnt1


