import cjson
infile='/spare/wei/folk/user_tag_dict_en_for_prob'
infile='/spare/wei/folk/user_tag_dict_sf'
outfile='/spare/wei/folk/user_tag_dict_en_for_prob_10'
outfile=open(outfile,'w')
for line in open(infile,'r'):：
    line=cjson.decode(line)
    v=0
    for key,value in line[1].iteritems():
        v+=value
   # print v
    if v>10:
        outfile.write(cjson.encode(line)+'\n')
    else:pass
