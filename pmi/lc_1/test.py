import cjson

infile=open('./gpd2_atlanta','r')
print len(cjson.decode(infile.readline()))
