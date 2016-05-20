import cjson
import math
from operator import itemgetter
earthRadiusMiles = 3958.761
target_loc=[[41.84,-87.68],[40.71,-73],[34.05,-118.24],[37.77,-122.42],[29.76,-95.36],[25.76,-80.19],[33.74,-84.38],[39.95,-75.16],[47.6,-122.3],[32.77,-96.8]]
name=['chicago','new york','la','sf','houston','miami','atlanta','indiana','seatle','dallas']
def getHaversineDistance(origin, destination, radius=earthRadiusMiles):
    lat1, lon1 = origin
    lat2, lon2 = destination
            #radius = 6371 # km
    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c
    return d
infilename='../data5'
for i in range(len(target_loc)):
    infile=open(infilename,'r')
    outfile=open('data_'+name[i],'w')
    for line in infile:
        line=cjson.decode(line)
        if getHaversineDistance(target_loc[i],[line['user_lat'],line['user_lng']])<100:
            outfile.write(cjson.encode(line)+'\n')
    outfile.close()
    infile.close()



