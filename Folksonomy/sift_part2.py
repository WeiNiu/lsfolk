import cjson
outfile='part2'
out=open(outfile,'w')
infile='rulelist_en_new_lt10_2_part2'
infile='rulelist_sf_part2'
for line in open(infile,'r'):
    line=cjson.decode(line)
#tiny topics    
    if line[2]>line[3] and line[3]>0.1 and line[2]<0.6 and line[2]>0.3:
        out.write(cjson.encode(line)+'\n')
#some phrases
    elif line[2]>line[3] and line[3]>0.6:
        out.write(cjson.encode(line)+'\n')
 
