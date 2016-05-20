#current not of much use since we have tagger and tag rule
import cjson
infile='/spare/wei/folk/tag_user_dict_sf'
outfile='/spare/wei/folk/tag_user_dict_sf_2'
outfile=open(outfile,'w')
for line in open(infile,'r'):：
    line=cjson.decode(line)
    if line[-1]>=2:
        outfile.write(cjson.encode(line)+'\n')
    else:pass
