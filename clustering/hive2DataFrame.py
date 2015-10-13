from __future__ import division, print_function
from sqlalchemy import create_engine, text
import pyhs2
import sasl
import re
import time
import datetime
import numpy as np
import pandas as pd


print ('------------PROCESS START---------------')
print (time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))

host = 'x.x.x.x'
port = 10000
auth = 'PLAIN'
user = 'xxx'
pswd = 'xxx'
daba = 'default'

#Fetch some user Ids 
query = '''SELECT mixpanel_map['  union user ID']
        FROM schema.table 
        WHERE group LIKE 'xxx' 
        AND mixpanel_map['  union user ID'] IS NOT NULL 
        AND mixpanel_map['App version on install'] IS NOT NULL
        AND mixpanel_map['App version on install'] != "<1.5"
        AND mixpanel_map['Install date'] >= "2015-08-01"
        AND mixpanel_map['Install date'] < "2015-09-01"
        AND mixpanel_map['time'] IS NOT NULL
        GROUP BY mixpanel_map['  union user ID']
        --DISTRIBUTE BY RAND()
        --SORT BY RAND()
        LIMIT 10000
        '''

with pyhs2.connect(host=host,port=port,authMechanism=auth,user=user,password=pswd,database=daba) as conn:
    with conn.cursor() as cur:
        cur.execute(query)
        user_IDs = [row[0] for row in cur.fetch()]

print ('------------JOIN STARTS---------------')
print (time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
#Get events created by above users
query = '''SELECT * FROM schema.table WHERE mixpanel_map['  union user ID'] IN('{ids}')'''.format(ids="','".join(user_IDs))
null = np.nan

print ('------------JOIN STARTS---------------')
print (time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
#Get events created by above users
null = np.nan
main_dict = []
with pyhs2.connect(host=host,port=port,authMechanism=auth,user=user,password=pswd,database=daba) as conn:
    with conn.cursor() as cur:
        #for i in range(100):
        #    print('Events of {} users queried'.format(i*100))
        #    uid = user_IDs[i*100:(i+1)*100]
        query = '''SELECT * FROM schema.table WHERE mixpanel_map['  union user ID'] IN('{ids}')'''.format(ids="','".join(user_IDs))
        cur.execute(query)
        for index, row in enumerate(cur.fetchall()):
        	if np.mod(index,1000)==0:
        		print('{} records queried'.format(index))
			event = row[0]
			year = row[len(row)-1]
			properties = eval(row[1])
			properties['event'] = event
			properties['year'] = year
			columns = properties.keys()
			values = properties.values()
			main_dict.append(properties) 


conn.close()
df = pd.DataFrame(main_dict)

print ('------------JOIN COMPLETE---------------')
print (time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))


print ('------------PROCESS COMPLETE---------------')
print (time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))

    
# Safe resulting DataFrame
df.to_pickle('df.pkl') 
