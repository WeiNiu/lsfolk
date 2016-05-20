import cjson


name=['chi','ny','la','sf','hou','miami','london','sydney','seattle','dallas']
name=['all']
target_loc=[[41.84,-87.68],[40.71,-73],[34.05,-118.24],[37.77,-122.42],[29.76,-95.36],[25.76,-80.19],[33.74,-84.38],[39.95,-75.16],[47.6,-122.3],[32.77,-96.8]]

#freq-based
for loc in name:
    outfile=open('rulelist_tfidf_new_'+loc,'w')
    infile=open('../../backbone/general1/cosine1-tfidf-'+loc,'r')
    cosdict=cjson.decode(infile.readline())
    #infile1=open('../backbone/tag_freq_dict_'+loc,'r')
    freqdict={}
    infile1=open('./centrality-tfidf-'+loc,'r')
    for line in infile1:
        line=cjson.decode(line)
        freqdict[line[0]]=line[1]
    #freqdict=cjson.decode(infile1.readline())
    for key,value in cosdict.iteritems():
        key1,key2=key.split('_')
        freqdict[key1]=freqdict.get(key1,0)
        freqdict[key2]=freqdict.get(key2,0)
        if freqdict[key1]<=freqdict[key2] and value >0.15:
            line=[key1,key2,value,freqdict[key1],freqdict[key2]]
            outfile.write(cjson.encode(line)+'\n')
        elif freqdict[key1]>freqdict[key2] and value>0.15:
            line=[key2,key1,value,freqdict[key1],freqdict[key2]]
            outfile.write(cjson.encode(line)+'\n')

