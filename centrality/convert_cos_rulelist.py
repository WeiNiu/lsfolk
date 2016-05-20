import cjson


name=['chicago','new_york','la','sf','houston','miami','atlanta','indiana','seatle','dallas']
target_loc=[[41.84,-87.68],[40.71,-73],[34.05,-118.24],[37.77,-122.42],[29.76,-95.36],[25.76,-80.19],[33.74,-84.38],[39.95,-75.16],[47.6,-122.3],[32.77,-96.8]]

#freq-based
for loc in name:
    outfile=open('rulelist_tfidf_'+loc,'w')
    infile=open('../backbone/cosine1-tfidf-'+loc,'r')
    cosdict=cjson.decode(infile.readline())
    infile1=open('../backbone/tag_freq_dict_'+loc,'r')
    freqdict=cjson.decode(infile1.readline())
    for key,value in cosdict.iteritems():
        key1,key2=key.split('_')
        if freqdict[key1]<=freqdict[key2]:
            line=[key2,key1,value]

        else:
            line=[key1,key2,value]
        outfile.write(cjson.encode(line)+'\n')

