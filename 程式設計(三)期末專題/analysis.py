from configparser import ConfigParser
import json
import pandas as pd

pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)
from package.subpackage1 import *
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['Taipei Sans TC Beta']
radius = 300
CITY = 'Kaohsiung'

config = ConfigParser()
config.read('token.ini', encoding='utf8')
app_id = config['token']['id']
app_key = config['token']['key']
googlemaps_key = config['googlemaps-token']['key']
p = auth.AuthPTX(app_id, app_key)
g = auth.AuthGooglemap(googlemaps_key)

'''====================
| 取得109行政區人口統計資料
===================='''
def getDemographicData():
    d = auth.DATA()
    response = d.request()
    data = json.loads(response.content)
    df = pd.DataFrame(data['result']['records'])
    df.to_csv('csv/109行政區人口資料.csv', encoding='utf_8_sig')
    return df

'''====================
| 取得高雄市公車站牌所在行政區(同位置多個站牌只算一個)
===================='''
import time
def getStationLocation():
    params= {
        # '$top': 1,
        '$format': 'JSON'
    }
    response = p.request(f'Station/City/{CITY}', params)
    if response.status_code == 200:
        df = pd.DataFrame(columns=['station_name'])
        data = json.loads(response.content)
        _list = set()
        for _ in data:
            _stationName = _['StationName']['Zh_tw']
            if _stationName not in _list:
                try:
                    lat = _["StationPosition"]["PositionLat"]
                    lng = _["StationPosition"]["PositionLon"]
                    latlng = f'{lat},{lng}'
                    response_ = dict() ; response_['status'] = 'OK'
                    response_ = g.get_geocode_uselatlng(latlng)
                    time.sleep(0.021) # Geocoding API 有 50 QPS(每秒請求數)限制，因此在迴圈增加 21ms 延遲
                    if response_['status'] == 'OK':
                        _list.add(_stationName)

                        compound_code = response_['plus_code']['compound_code']
                        columns = {
                            'station_name': _stationName,
                            'lat': lat,
                            'lng': lng, 
                            'district': compound_code
                        }
                        new_row = pd.DataFrame(columns, index=[0])
                        print(new_row)
                        df = df.append(new_row, ignore_index=True)
                    else:
                        print(response_)
                        df.to_csv('csv/高雄市公車站牌.csv', encoding='utf_8_sig')
                        quit()
                except Exception as e:
                    print(e)
            
                    
        
        print(df)
        df.to_csv('csv/高雄市公車站牌.csv', encoding='utf_8_sig')
        return df
        
    else:
        print(response.status_code)
    
'''====================
| 取得公車站牌數量以行政區劃分
===================='''
def getStationCountGroupByDistrict():
    df = pd.read_csv('csv/高雄市公車站牌.csv')
    df['district'] = df['district'].apply(lambda x: x[x.find('高雄市'):])

    df = df.groupby(['district'])['district'].count().reset_index(name='count')
    _ = {
        'district': '高雄市',
        'count': df['count'].sum()
    }
    total_row = pd.DataFrame(_, index=[0])
    df = df.append(total_row, ignore_index=True)
    df.to_csv('csv/行政區公車站位統計.csv', encoding='utf_8_sig')
    print(df)
    return df

'''====================
| 繪製圖形：公車站牌數量以行政區劃分
===================='''
def show():
    df = getStationCountGroupByDistrict()
    df.sort_values('count')[['district', 'count']].plot(x="district", y="count", kind="barh",figsize=(16,9))
    plt.title('各行政區公車站牌數量')
    plt.show()


def getAllData():
    df1 = pd.read_csv('csv/109人口密度.csv')
    df1 = df1[['site_id', 'people_total', 'area', 'population_density']]
    bool_ = df1['site_id'].str.startswith('高雄市', na=False)
    df1 = df1.loc[bool_]

    df2 = getStationCountGroupByDistrict()
    df1 = df1.merge(df2, how='left', left_on='site_id', right_on='district')
    newColumnName = {
        'site_id': '行政區', 
        'people_total': '人口數', 
        'area': '土地面積', 
        'population_density': '人口密度', 
        'count': '公車站牌數'
    }
    df1 = df1.rename(columns=newColumnName)
    df1['人口數'] = pd.to_numeric(df1['人口數'])
    df1 = df1.drop(columns=['district'])

    df1['公車站牌數'] = df1['公車站牌數'].fillna(0) #convert NaN to 0
    df1['公車站牌數'] = df1['公車站牌數'].map('{:.0f}'.format)
    df1 = df1.rename(columns=newColumnName)
    df1['公車站牌數'] = pd.to_numeric(df1['公車站牌數'])

    df1['N個人分配一個公車站牌'] = df1['人口數'] / df1['公車站牌數']
    df1['N個人分配一個公車站牌'] = df1['N個人分配一個公車站牌'].map('{:,.2f}'.format)
    print(df1)
