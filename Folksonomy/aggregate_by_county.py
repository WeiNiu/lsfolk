import cjson,re
from collections import defaultdict
statename_dict={'Mississippi': 'MS', 'Oklahoma': 'OK', 'Delaware': 'DE', 'Minnesota': 'MN', 'Illinois': 'IL', 'Arkansas': 'AR', 'New Mexico': 'NM', 'Indiana': 'IN', 'Maryland': 'MD', 'Louisiana': 'LA', 'Idaho': 'ID', 'Wyoming': 'WY', 'Tennessee': 'TN', 'Arizona': 'AZ', 'Iowa': 'IA', 'Michigan': 'MI', 'Kansas': 'KS', 'Utah': 'UT', 'Virginia': 'VA', 'Oregon': 'OR', 'Connecticut': 'CT', 'Montana': 'MT', 'California': 'CA', 'Massachusetts': 'MA', 'West Virginia': 'WV', 'South Carolina': 'SC', 'New Hampshire': 'NH', 'Wisconsin': 'WI', 'Vermont': 'VT', 'Georgia': 'GA', 'North Dakota': 'ND', 'Pennsylvania': 'PA', 'Florida': 'FL', 'Alaska': 'AK', 'Kentucky': 'KY', 'Hawaii': 'HI', 'Nebraska': 'NE', 'Missouri': 'MO', 'Ohio': 'OH', 'Alabama': 'AL', 'Rhode Island': 'RI', 'South Dakota': 'SD', 'Colorado': 'CO', 'New Jersey': 'NJ', 'Washington': 'WA', 'North Carolina': 'NC', 'New York': 'NY', 'Texas': 'TX', 'Nevada': 'NV', 'Maine': 'ME'}
county_count_dict=defaultdict(dict)
infile = '/spare/wei/folk/list_creator_user_addr_tech_us'
count=0
for line in open(infile,'r'):
    line=cjson.decode(line)
    addr=line['c_addr']
    #print addr
    state=''
    county=''
    if addr['c_code']=='us'and 'c' in addr.keys():
        if addr['c']=='District of Columbia':
            state='DC'
            county='Washington'
        elif 's' in addr.keys():
            state=addr['s']
       #     print state
            if state in statename_dict.keys():
                state_abbr=statename_dict[state]
               # print state_abbr
            else: continue
            county=re.split(' (city)| Census Area| City and County| County',addr['c'])[0]
        else: continue
        if county not in county_count_dict[state_abbr].keys():
            county_count_dict[state_abbr][county]=1
        else:
            county_count_dict[state_abbr][county]+=1
        count+=1
for key,value in county_count_dict.iteritems():
    print key,value
outfile='/spare/wei/folk/tech_creator_count_by_county_us'
out=open(outfile, 'w')
out.write(cjson.encode(county_count_dict))
print count             

