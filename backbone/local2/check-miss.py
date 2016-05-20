import cjson
ky=[]
for line in open('folk-c-new_york','r'):
    line=line.strip(' ')
    line=line.split('\n')[0]
    ky.append(line)
print len(ky)
infile1=open('gpd-combine-new_york','r')
line=cjson.decode(infile1.readline())
for key in line:
    if key not in ky:
        print key

