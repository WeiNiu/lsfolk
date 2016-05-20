from pattern.en import parse
import cjson
import sys

#gpd   removelist
infile1=open(sys.argv[1],'w')
infile2=open(sys.argv[2],'r')
removelist=cjson.decode(infile2.readline())
infile2.close()
for key,value in cjson.decode(infile1.readline()):
    if ' ' in key:
        d= parse(key).split()[0]
        if d[0][1]!='NN' and d[1][1]!='NN':
            removelist.append(key)
            print key
        else:
            pass
    else:
        d=parse(key).splist()[0]
        if d[0][1]!='NN':
            removelist.append(key)
            print key
        else:pass
infile3=open(sys.argv[2],'w')
infile3.write(cjson.encode(removelist))

