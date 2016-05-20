import cjson
ky=[]
for line in open('folk_cen_noise_atlanta','r'):
    line=line.strip(' ')
    line=line.split('\n')[0]
    ky.append(line)
print len(ky)
infile1=open('gpd2_atlanta','r')
line=cjson.decode(infile1.readline())
for key in line:
    if key not in ky:
        print key

