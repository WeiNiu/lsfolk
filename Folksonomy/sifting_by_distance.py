import cjson
from library.geo import getHaversineDistance


infile='/spare/wei/folk/list_creator_user_location_en_new'
#infile='/spare/wei/folk/dist_greater_than_500'
def getHDfromUTMLL(u1,u2, radius):
    lat1,long1,_=u1.split('_')
    corr1=(float(lat1),float(long1))
    lat2,long2,_=u2.split('_')
    corr2=(float(lat2),float(long2))
    dist=getHaversineDistance(corr1,corr2,radius)
    return dist
earthRadiusMiles = 3958.761
outfile='/spare/wei/folk/dallas_tagging'
#outfile1='/spare/wei/folk/dist_greater_than_50_less_than_500_2'
#outfile2='/spare/wei/folk/dist_greater_than_500_less_than_3000_2'
#outfile3='/spare/wei/folk/dist_greater_than_3000_2'
outfile=open(outfile,'w')
#outfile1=open(outfile1,'w')
#outfile2=open(outfile2,'w')
#outfile3=open(outfile3,'w')
for line in open(infile,'r'):
    line = cjson.decode(line)
    lat_u,lng_u=line['user_lat'],line['user_lng']
    lat_c,lng_c = 32.78014,-96.800451
   # lat_c,lng_c=line['list_creator_lat'],line['list_creator_lng']
   # lat_c,lng_c = 40.705631,-73.978003
   # lat_c,lng_c = 37.77493,-122.419416
   # lat_c,lng_c=29.760193,-95.36939
   # lat_c,lng_c = 30.627977,-96.334407
    dist = getHaversineDistance([lat_u,lng_u],[lat_c,lng_c],earthRadiusMiles)
    if dist <= 20:
        outfile.write(cjson.encode(line)+'\n')
#    elif dist>50 and dist<500:
#        outfile1.write(cjson.encode(line)+'\n')
#    elif dist>500 and dist<3000:
#        outfile2.write(cjson.encode(line)+'\n')
#    else:
#        outfile3.write(cjson.encode(line)+'\n')

