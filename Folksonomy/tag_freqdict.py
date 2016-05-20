import cjson
infile='/spare/wei/local/tag_user_dict_ch3'
tag_f={}
cnt=0
lin=''
for line in open(infile,'r'):
#    line=line.split('\t')[1]
    line=cjson.decode(line)
    tag_f[line[0]]=line[-1]
    if cnt<line[-1]:
        cnt=line[-1]
        lin=line[0]
outfile='/spare/wei/local/tag_freq_dict_ch3'
outfile=open(outfile,'w')
outfile.write(cjson.encode(tag_f))
print lin,cnt
