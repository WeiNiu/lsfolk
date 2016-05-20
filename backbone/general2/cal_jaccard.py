from __future__ import division
import cjson
import sys
infile1=open(sys.argv[1],'r')
infile2=open(sys.argv[2],'r')
dict1=cjson.decode(infile1.readline())
dict2=cjson.decode(infile2.readline())
n=len((set(dict1.keys())).intersection(set(dict2.keys())))
m=len((set(dict1.keys())).union(set(dict2.keys())))
key=str(sys.argv[1]).split('_')[-1]+str(sys.argv[2]).split('_')[-1]
outfile=open(sys.argv[3],'a')
outfile.write(cjson.encode([key,n/m])+'\n')
