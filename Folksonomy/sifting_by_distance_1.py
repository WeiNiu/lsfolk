from __future__ import division
import cjson
from library.geo import getHaversineDistance


infile='/spare/wei/folk/list_creator_user_location_all_new'#'/spare/wei/folk/list_creator_user_location_en_20_1000'
#infile='/spare/wei/folk/dist_greater_than_500'
dist_dict={}
def getHDfromUTMLL(u1,u2, radius):
    lat1,long1,_=u1.split('_')
    corr1=(float(lat1),float(long1))
    lat2,long2,_=u2.split('_')
    corr2=(float(lat2),float(long2))
    dist=getHaversineDistance(corr1,corr2,radius)
    return dist
earthRadiusMiles = 3958.761
outfile='/spare/wei/folk/dist_dict_all'
#outfile1='/spare/wei/folk/dist_lt_40_en'
#outfile2='/spare/wei/folk/dist_lt_50_en'
#outfile3='/spare/wei/folk/dist_greater_than_3000_2'
outfile=open(outfile,'w')
#outfile1=open(outfile1,'w')
#outfile2=open(outfile2,'w')
#outfile3=open(outfile3,'w')
for line in open(infile,'r'):
    line = cjson.decode(line)
    lat_u,lng_u=line['user_lat'],line['user_lng']
    lat_c,lng_c=line['list_creator_lat'],line['list_creator_lng']
    dist=getHaversineDistance([lat_u,lng_u],[lat_c,lng_c],earthRadiusMiles)
#    if dist <= 30:
#        outfile.write(cjson.encode(line)+'\n')
#    if dist<=40:
#        outfile1.write(cjson.encode(line)+'\n')
#    if dist<=50:
#        outfile2.write(cjson.encode(line)+'\n')
#    else:
#        outfile3.write(cjson.encode(line)+'\n')
    dist=int(dist/10)*10
    dist_dict[str(dist)]=dist_dict.get(str(dist),0)+1
outfile.write(cjson.encode(dist_dict)+'\n')
