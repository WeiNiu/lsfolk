import cjson
list=['social medium', 'medium', 'social', 'twibe marketing','twibe', 'tweeter']
outfile=open('./remove','w')
outfile.write(cjson.encode(list))

