from __future__ import division, print_function
import re
import time
import datetime
import numpy as np
import pandas as pd


#vacation???
#which features can actually be utilized by marketing/crm/product? restrict to those or not???
#make binary features out of nominal by asking is_t-mobile, is_o2, ... test = df['$city'].unique()#res = pd.get_dummies(test)#http://stackoverflow.com/questions/32387266/converting-categorical-values-to-binary-using-pandas

# check is west germany again!!
# mp_device_model=model??
#live tv per live span >1!!!
#check if not logged in','UserStatusNotSigned' means not registered!
# check if majority vote weekpart, daytime is correct!

# Read DateFrame
df = pd.read_pickle('df.pkl')    


# Join columns with ones for counting
df['ones'] = 1.


# Time needs to be float for futher processing
df.time = np.float32(df.time) # timestamp needs to be float
df = df[np.isfinite(df.time)] # time should be given


# Create DataFrame with user IDs
c = pd.DataFrame(df['P7S1 user ID'].unique(), columns=['P7S1 user ID'])


# 'watched_x_count' where x is in top 5 formats
d = 'Content format name'
f = 'watched_x_count where x is in top 5 formats'
print('Extracting {}'.format(f))
F = []
df_tmp = df[[d,'ones']].groupby(by=['Content format name'], as_index=False).sum()
top_5_list = df_tmp.sort(['ones'])[-5:]['Content format name'].tolist()
m = df[['P7S1 user ID',d,'ones']].groupby(by=['P7S1 user ID',d], as_index=False).sum()
for fmt in top_5_list:
    f = 'watched_' + fmt + '_count'
    F.append(f)
    m_tmp = m[m[d]==fmt][['P7S1 user ID','ones']]
    m_tmp.columns = ['P7S1 user ID',f]
    c = pd.merge(c, m_tmp, on=['P7S1 user ID'], how='left')
    c[f] = c[f].fillna(0)

c[F] = c[F].div(c[F].sum(axis=1), axis=0).fillna(0)
    
    
# 'watched_x_count' where x is in unique channels
d = 'Channel name'
f = 'watched_x_count where x is in unique channels
print('Extracting {}'.format(f))
F = []
x = np.array([type(s)==str for s in df[d].unique()])
Chn = df[d].unique()[x]
m = df[['P7S1 user ID',d,'ones']].groupby(by=['P7S1 user ID',d], as_index=False).sum()
for chn in Chn:
    f = 'watched_' + chn + '_count'
    F.append(f)
    m_tmp = m[m[d]==chn][['P7S1 user ID','ones']]
    m_tmp.columns = ['P7S1 user ID',f]
    c = pd.merge(c, m_tmp, on=['P7S1 user ID'], how='left')
    c[f] = c[f].fillna(0)

c[F] = c[F].div(c[F].sum(axis=1), axis=0).fillna(0)


# 'main_activity_daytime' 0: 4-10, 1: 10-14, 2: 14-22, 3: 22-4, -1: else
f = 'main_activity_daytime'
print('Extracting {}'.format(f))
d = 'time'
c[f] = -1
df_sub = df[['P7S1 user ID',d]]
for i in c['P7S1 user ID']:
    T = df_sub[df_sub['P7S1 user ID']==i].time.tolist()
    h = []
    for t in T:
        try:
            h.append(datetime.datetime.fromtimestamp(t).hour)
        except:
            continue
    try:
        x, bins = np.histogram(h, bins=[0,4,10,16,22])
        day_time = np.argmax(x)
        c[f][c['P7S1 user ID']==i] = day_time
    except:
        c[f][c['P7S1 user ID']==i] = -1
        continue
c[f] = c[f].fillna(-1)
        
         
# 'main_activity_weekpart' 0: 0-4, 1: 5-6, -1: else
f = 'main_activity_weekpart'
print('Extracting {}'.format(f))
d = 'time'
c[f] = -1
df_sub = df[['P7S1 user ID',d]]
for i in c['P7S1 user ID']:
    T = df_sub[df_sub['P7S1 user ID']==i].time.tolist()
    h = []
    for t in T:
        try:
            h.append(datetime.datetime.fromtimestamp(t).weekday())
        except:
            continue
    try:
        x, bins = np.histogram(h, bins=[0,5,6])
        week_part = np.argmax(x)
        c[f][c['P7S1 user ID']==i] = week_part
    except:
        c[f][c['P7S1 user ID']==i] = -1
        continue
c[f] = c[f].fillna(-1)


# 'main_activity_season' 0: Dec-Feb , 1: Mar-May, 2: June-Aug, 3: Sept-Nov, -1: else
f = 'main_activity_season'
print('Extracting {}'.format(f))
d = 'time'
c[f] = -1
df_sub = df[['P7S1 user ID',d]]
for i in c['P7S1 user ID']:
    T = df_sub[df_sub['P7S1 user ID']==i].time.tolist()
    h = []
    for t in T:
        try:
            h.append(datetime.datetime.fromtimestamp(int(t)).month)
        except:
            continue
    try:
        x, bins = np.histogram(h, bins=[1,3,6,9,11])
        season = np.argmax(x)
        c[f][c['P7S1 user ID']==i] = season
    except:
        c[f][c['P7S1 user ID']==i] = -1
        continue
c[f] = c[f].fillna(-1)


# Sessions
f = 'sessions'
print('Extracting {}'.format(f))
d = '[Retention] New session started'
m = df[df.event==d][['P7S1 user ID','ones']].groupby(by=['P7S1 user ID'], as_index=False).sum()
m.columns = ['P7S1 user ID', f]
c = pd.merge(c, m, on=['P7S1 user ID'], how='left')
c[f] = c[f].fillna(0)


# Per-session features
features = ['clicks_per_session', 
            'videoviews_per_session',
            'searches_per_session',
            'shares_per_session',
            'watchlaterclicks_per_session',
            'remindmeclicks_per_session',
            'favoritclicks_per_session',
            'adclicks_per_session',
            'feedbacks_per_session'
           ]

columns = ['[Action] Opened view', 
			'[Action] Video content view started',
            '[Action] Search used',
            '[Referral] Share item clicked',
        	'[Retention] Watch later clicked',
            '[Retention] Remind me clicked',
            '[Retention] Favorite clicked',
            '[Action] Video Ad clicked',
            '[Action] Feedback clicked'
            ]

for d, f in zip(columns,features):
	print('Extracting {}'.format(f))
    m = df[df.event==d][['P7S1 user ID','ones']].groupby(by=['P7S1 user ID'], as_index=False).sum()
    m.columns = ['P7S1 user ID', f]
    c = pd.merge(c, m, on=['P7S1 user ID'], how='left')
    c[f] = c[f].div(c.sessions)
    c[f] = c[f].replace(np.inf, 0)
    c[f] = c[f].replace(-np.inf, 0)
    c[f] = c[f].fillna(0)    
    
    
# Average session durations
D = ['Last session gross length','Last session net length']
F = ['avg_session_gross_length','avg_session_net_length']
e = '[Retention] New session started'
for d, f in zip(D,F):
	print('Extracting {}'.format(f))
    m = df[df.event==e][['P7S1 user ID',d]]
    m[d] = m[d].fillna(0)
    m[d][m[d]=='undefined'] = -1
    m[d] = np.float32(m[d])
    m = m.groupby(by='P7S1 user ID', as_index=False).sum()
    m.columns = ['P7S1 user ID', f]
    c = pd.merge(c, m, on=['P7S1 user ID'], how='left')
    c[f] = c[f].fillna(0)
    c[f] = c[f].div(c.sessions)
    c[f] = c[f].replace(np.inf, 0)
    c[f] = c[f].fillna(0)	
	

# 'live_view_duration_per_session'
f = 'live_view_duration_per_session'
print('Extracting {}'.format(f))
d = 'Total Live TV time (s)'
e = '[Action] Finished watching Live TV'
#m = df[df.event==e][['P7S1 user ID',d]]
#m.fillna(0)
#m[d] = np.float32(m[d])
#m = m.groupby(by='P7S1 user ID', as_index=False).max()
#m.columns = ['P7S1 user ID', f]
#c = pd.merge(c, m, on=['P7S1 user ID'], how='left')
#c[f] = c[f].div(c.sessions)
#c[f] = c[f].replace(np.inf, 0)
#c[f] = c[f].replace(-np.inf, 0)
#c[f] = c[f].fillna(0)


# 'live_view_times_per_session'
f = 'live_view_times_per_session'
print('Extracting {}'.format(f))
d = 'Total Live TV time (s)'
e = '[Action] Finished watching Live TV'
#m = df[df.event==e][['P7S1 user ID','ones']]
#m.fillna(0)
#m[d] = np.float32(m[d])
#m = m.groupby(by='P7S1 user ID', as_index=False).sum()
#m.columns = ['P7S1 user ID', f]
#c = pd.merge(c, m, on=['P7S1 user ID'], how='left')
#c[f] = c[f].div(c.sessions)
#c[f] = c[f].replace(np.inf, 0)
#c[f] = c[f].replace(-np.inf, 0)
#c[f] = c[f].fillna(0)
  

# Live span, i.e. the duration between first and last (known) session (in seconds)
# alternatively also available: Day count since install
f = 'life_span'
print('Extracting {}'.format(f))
m = df[['P7S1 user ID','time']].groupby(by=['P7S1 user ID'], as_index=False).max()
m.columns = ['P7S1 user ID','max_time']
m_ = df[['P7S1 user ID','time']].groupby(by=['P7S1 user ID'], as_index=False).min()
m_.columns = ['P7S1 user ID','min_time']
m[f] = (m.max_time - m_.min_time)/3600/24 #seconds to days
m = m[['P7S1 user ID', f]]
c = pd.merge(c, m, on=['P7S1 user ID'], how='left')
c[f] = c[f].fillna(0)


# Life span per time since install
f = 'life_span_per_time_since_install'
print('Extracting {}'.format(f))
m = df[['P7S1 user ID','time']].groupby(by=['P7S1 user ID'], as_index=False).min()
m[f] = (time.time() - m.time)
m = m[['P7S1 user ID',f]]
c = pd.merge(c, m, on=['P7S1 user ID'], how='left')
c[f] = c[f].fillna(0)
c[f] = c.life_span.div(c[f])
c[f] = c[f].replace(np.inf, 0)


# Sessions per life span
f = 'sessions_per_life_span'
print('Extracting {}'.format(f))
c[f] = c.sessions.div(c.life_span)
c[f] = c[f].replace(np.inf, 0)
c[f] = c[f].fillna(0)


# Other features: 'is_reg'
f = 'is_reg'
print('Extracting {}'.format(f))
d = 'P7S1 user status'
m = df[['P7S1 user ID',d]]
m.columns = ['P7S1 user ID', f]
for r in ['not logged in','UserStatusNotSigned']:
    m[f][df['P7S1 user status']==r] = 0
    
for r in ['logged in','pending', 'UserStatusSignedIn']:
    m[f][df['P7S1 user status']==r] = 1

m[f] = m[f].fillna(-1)
m = m.groupby(['P7S1 user ID'],as_index=False).max()
c = pd.merge(c, m, on=['P7S1 user ID'], how='left')
c[f] = c[f].fillna(-1)


# Other features: 'is_west_germany'
east = ['Thuringia', 
		'Saxony', 
		'Saxony-Anhalt', 
		'Brandenburg', 
		'Mecklenburg-Vorpommern']
west = ['Land Berlin',
		'North Rhine-Westphalia', 
		'Baden-W\xc3\xbcrttemberg Region',  
		'Rheinland-Pfalz', 
		'Hesse', 
		'Saarland', 
		'Lower Saxony',
		'Bavaria', 
		'Bremen',
		'Hamburg', 
		'Schleswig-Holstein']
f = 'is_west_germany'
print('Extracting {}'.format(f))
d = '$region'
m = df[['P7S1 user ID',d]]
m[f] = -1
for r in east:
    m[f][m[d]==r] = 0
    
for r in west:
    m[f][m[d]==r] = 1

m = m[['P7S1 user ID',f]]
m = m.groupby(['P7S1 user ID'],as_index=False).max()
c = pd.merge(c, m, on=['P7S1 user ID'], how='left')
c[f] = c[f].fillna(-1)


# Other features: 'avg_prop_watched', 'avg_video_length'
F = ['avg_prop_watched','avg_video_length']
D = ['View time to content length ratio (%)','Content video length (s)']
V = ['[Action] Finished watching video','[Action] Finished watching video']
#for f, d, v in zip(F,D,V):
#	print('Extracting {}'.format(f))
#	m = df[['P7S1 user ID',d]][df.event==v]
#	m.columns = ['P7S1 user ID',f]
#	m[f] = m[f].fillna('0')
#	for row_index, row in m.iterrows():
#			m[f][row_index] = re.sub(',', '.', row[f])
#	m[f] = m[f].fillna(0)
#	m[f] = np.float32(m[f])
#	if f=='avg_prop_watched':
#		m[f] *= .01
#	m = m.groupby(by=['P7S1 user ID'], as_index=False).mean()
#	c = pd.merge(c, m, on=['P7S1 user ID'], how='left')
#	c[f] = c[f].replace(np.inf, 0)
#	c[f] = c[f].fillna(0)


# Other features: 'has_re-enabled_opt-in'
f = 'has_re-enabled_opt-in'
print('Extracting {}'.format(f))
d = '[Action] Tracking Opt-In'
m = df[df.event==d][['P7S1 user ID','ones']].groupby(by=['P7S1 user ID'], as_index=False).sum()
m.columns = ['P7S1 user ID', f]
m[f] = 1
c = pd.merge(c, m, on=['P7S1 user ID'], how='left')
c[f] = c[f].fillna(0)


# Other features: 'formats_watched_per_session', 'channels_per_session'
F = ['formats_watched_per_session', 'channels_watched_per_session']
D = ['Content format ID', 'Channel name']
for f, d in zip(F,D):
	print('Extracting {}'.format(f))
	m = df[['P7S1 user ID',d,'ones']].groupby(by=['P7S1 user ID',d,'ones'], as_index=False).sum().dropna()
	m.ones = 1
	m = m[['P7S1 user ID','ones']].groupby(by=['P7S1 user ID'], as_index=False).sum()
	m.columns = ['P7S1 user ID', f]
	c = pd.merge(c, m, on=['P7S1 user ID'], how='left')
	c[f] = c[f].fillna(0)
	c[f] = c[f].div(c.sessions)
	c[f] = c[f].replace(np.inf, 0)
	c[f] = c[f].fillna(0)


# Other features: 'has_seen_tac', 'has_seen_faq', 'has_seen_live_info', 'has_seen_infoprivacy', 'has_seen_impressum'
F = ['has_seen_tac', 'has_seen_faq','has_seen_live_info','has_seen_infoprivacy','has_seen_impressum']
V = ['AGB','Hilfe & FAQ','Infos zu Live TV','Datenschutz','Impressum']
#d = 'Local HTML Title'
#for f, v in zip(F,V):
#	print('Extracting {}'.format(f))
#	m = df[df[d]==v][['P7S1 user ID','ones']].groupby(by=['P7S1 user ID'], as_index=False).sum()
#	m.columns = ['P7S1 user ID', f]
#	m[f] = 1
#	c = pd.merge(c, m, on=['P7S1 user ID'], how='left')
#	c[f] = c[f].fillna(0)


# Other features: 'push_enabled', 'has_nfc', 'has_telephone', 'has_wifi'
F = ['push_enabled','has_nfc', 'has_telephone', 'has_wifi', 'autostart']
D = ['Push enabled','$has_nfc', '$has_telephone', '$wifi', 'Autostart']
#for f, d in zip(F,D):
#	print('Extracting {}'.format(f))
#	df[d][df[d]=='true'] = 1
#	df[d][df[d]=='false'] = 0
#	df[d][(df[d]!=True)&(df[d]!=False)] = -1
#	m = df[['P7S1 user ID',d]].groupby(by=['P7S1 user ID'], as_index=False).max()
#	m = m.dropna()
#	m.columns = ['P7S1 user ID', f]
#	m[f] = np.int_(m[f])
#	c = pd.merge(c, m, on=['P7S1 user ID'], how='left')
#	c[f] = c[f].fillna(-1)
	
	
# Other features: 'pixels'
f = 'pixels'
print('Extracting {}'.format(f))
df[f] = np.int_(df['$screen_height'])*np.int_(df['$screen_width'])
m = df[['P7S1 user ID',f]].groupby(by=['P7S1 user ID'], as_index=False).max()
m = m.dropna()
c = pd.merge(c, m, on=['P7S1 user ID'], how='left')
c[f] = c[f].fillna(-1)


# Other features: ? 'ai_count', 'count', 'counter'
F = ['ai_count', 'count', 'counter']
D = ['AI count', 'Count', 'Counter']
#for f, d in zip(F,D):
#	print('Extracting {}'.format(f))
#	m = df[['P7S1 user ID',d]].groupby(by=['P7S1 user ID'], as_index=False).max()
#	m = m.dropna()
#	m.columns = ['P7S1 user ID', f]
#	m[f] = np.int_(m[f])
#	c = pd.merge(c, m, on=['P7S1 user ID'], how='left')
#	c[f] = c[f].fillna(-1)


# Other features: 'city_size'
f = 'city_size'
print('Extracting {}'.format(f))
d = '$city'

df_city = pd.io.parsers.read_csv('cityPeople.txt', sep='\t', encoding='ISO-8859-1')
df_city = df_city[df_city.columns[[0,6]]]
df_city.columns = [d, f]
mask = np.array([bool(np.mod(i,2)) for i in range(len(df_city))])
mask[400:] = False
df_city = df_city.iloc[mask,:]
for row_index, row in df_city.iterrows():
    r = re.sub(r'\[.+?\]\s*', '', row.city_size)
    df_city.city_size[row_index] = int(re.sub(r'\.','',r))

m = df[['P7S1 user ID',d]].groupby(by=['P7S1 user ID'], as_index=False).max()
m = m.dropna()
m[d] = np.array(m[d]).astype('U')
m[d][m[d]==u'Munich'] = u'Munchen'
m = pd.merge(m, df_city, on=[d], how='left')
m[f] = m[f].fillna(-1)
m = m[['P7S1 user ID', f]]
c = pd.merge(c, m, on=['P7S1 user ID'], how='left')
c[f] = c[f].fillna(-1)


# Other features: '$screen_dpi'
d = '$screen_dpi'
m = df[['P7S1 user ID',d]].groupby(by=['P7S1 user ID'], as_index=False).sum()
m[d] = np.float32(m[d].fillna(-1))
c = pd.merge(c, m, on=['P7S1 user ID'], how='left')
c[f] = c[f].fillna(-1)


# Mapping categorical features to binary ones
df['$brand'][df['$brand']=='HUAWEI'] = 'Huawei' #cleaning some duplicates
df['$carrier'][df['$carrier']=='o2 - de'] = 'o2-de'
cat_feat  =  ['$brand',
			  '$carrier',
			  '$google_play_services',
			  '$lib_version',
			  '$manufacturer',
			  '$model',
			  '$os',
			  '$os_version',
			  '$radio',
              '$region',
              'Device kind',
              '[Adjust.io] Campaign on install',
              'mp_device_model'
             ]        
top = 5
for d in cat_feat:
    f = 'rest_'+d
    print('Extracting {}'.format(f))
    c = pd.merge(c, df[['P7S1 user ID',d]], on=['P7S1 user ID'], how='left')
    top_list = c[d].value_counts().index.tolist()[:top]
    m = pd.get_dummies(c[d])
    oth_list = list(set(m.columns)-set(top_list))
    m = pd.concat([m[top_list], m[oth_list].sum(axis=1)], axis=1)
    m.columns = top_list+[f]
    c = pd.concat([c, m], axis=1, join_axes=[c.index])
    c[f] = c[f].fillna(1)


# Safe resulting DataFrame
c.to_pickle('df_clustering.pkl') 