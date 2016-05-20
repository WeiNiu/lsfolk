import cjson

infile=open('./tag_freq_dict_houston','r')
print len(cjson.decode(infile.readline()))
