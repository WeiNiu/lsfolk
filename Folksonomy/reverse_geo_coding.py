import sys,cjson, urllib2
#http://nominatim.openstreetmap.org/reverse?format=xml&lat=52.5487429714954&lon=-1.81602098644987&zoom=18&addressdetails=1
#import requests
#r=requests.post(std)
#for line in r.iter_lines():
#    line=cjson.decode(line)
#    print line
#    print line.keys()
#    print line['address']['county']
infile = '/spare/wei/folk/listings_us'#list_creator_user_location_nonsingular_100'
outfile='/spare/wei/folk/list_creator_user_addr_us'
web='http://nominatim.openstreetmap.org/reverse?format=json'
web='http://open.mapquestapi.com/nominatim/v1/reverse.php?format=json'
extra='&zoom=%2018&addressdetails=1'
outfile=open(outfile,'w')
for line in open(infile,'r'):
    line=cjson.decode(line)  
    #print line['tag']
#    if 'tech' in line['tag'] or 'technology' in line['tag']:
#        print line['tag']
    lat_1=line['list_creator_lat']
    lon_1=line['list_creator_lng']
    lat_2=line['user_lat']
    lon_2=line['user_lng']
    creator_lat='&lat='+str(lat_1)
    creator_lon='&lon='+str(lon_1)
    user_lat='&lat='+str(lat_2)
    user_lon='&lon='+str(lon_2)
    try:
        creator_url=web+creator_lat+creator_lon#+extra
#            print creator_url
        creator_info = urllib2.urlopen(creator_url)
        #print creator_info
        creator_info = creator_info.read()
        #print creator_info
        creator_addr=cjson.decode(creator_info)['address']
        #except:
        #    continue
#            print creator_addr
        new_creator_addr={}
        new_creator_addr['c_code']=creator_addr['country_code']
        if 'state' in creator_addr.keys():
            new_creator_addr['s']=creator_addr['state']
        if 'county' in creator_addr.keys():
            new_creator_addr['c']=creator_addr['county']
        line['c_addr']=new_creator_addr
        
        user_url=web+user_lat+user_lon#+extra
        user_info = urllib2.urlopen(user_url)
        user_info = user_info.read()
        user_addr=cjson.decode(user_info)['address']
#            print user_addr
        new_user_addr={}
        new_user_addr['c_code']=user_addr['country_code']
        if 'state' in user_addr.keys():
            new_user_addr['s']=user_addr['state']
        if 'county' in user_addr.keys():
            new_user_addr['c']=user_addr['county']
        line['u_addr']=new_user_addr
        line = cjson.encode(line)
        outfile.write(line+'\n')
    except:
        print "error reading web"
        #pass
        #sys.exit()
##else:
#        pass
#from httplib2 import Http
#h=Http()
#resp,content=h.request(std,'GET')
#content=cjson.decode(content)
#print content['county']
