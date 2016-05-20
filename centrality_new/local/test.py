import cjson

infile=open('./gpd_atlanta','r')
print len(cjson.decode(infile.readline()))
