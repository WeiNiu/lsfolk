import cjson
infile='/spare/wei/folk/list_creator_user_location_all_new'
#infile='/mnt/chevron/wei/list_creator_user_location_nonsingular_100'
#infile='/spare/wei/folk/listings_us_new'
#outfile1='/spare/wei/folk/listings_us_new'
outfile1='/spare/wei/folk/nutrition_listing_us_j_1'
outfile1=open(outfile1,'w')
#outfile2=open(outfile2,'w')

#--------------GET ALL LISTING IN US-----------------
def in_box_us(lat,lon):
    if lat>24.52 and lat<49.38 and lon<-66.95 and lon>-124.77:
        return 1
    elif lat>54.66 and lat<71.83 and ((lon<-130 and lon>-180) or (lon>173 and lon<180)):
        return 1
    else:
        return 0
#for line in open(infile,'r'):
#    line1=cjson.decode(line)
#    #if 'entertain'in line1['tag'] or 'entertainment' in line1['tag']:
#    lat_u=line1['user_lat']
#    lon_u=line1['user_lng']
#    lat_c=line1['list_creator_lat']
#    lon_c=line1['list_creator_lng']
#    if in_box_us(lat_u,lon_u)==1 or in_box_us(lat_c,lon_c)==1:
#        outfile1.write(line)


for line in open(infile,'r'):
    line1=cjson.decode(line)
#    if 'tech' in line1['tag']  or 'techy' in line1['tag'] or 'technology' in line1['tag']:
    #if 'entertain' in line1['tag']  or 'entertainment' in line1['tag'] or 'entertaining' in line1['tag'] or 'entertainer' in line1['tag']
    if 'nutrition' in line1['tag']:
        lat_u=line1['user_lat']
        lon_u=line1['user_lng']
        lat_c=line1['list_creator_lat']
        lon_c=line1['list_creator_lng']
        if in_box_us(lat_u,lon_u)==1 or in_box_us(lat_c,lon_c)==1:
            outfile1.write(line)

           
