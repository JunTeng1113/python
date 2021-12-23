from configparser import ConfigParser
from hashlib import new
import json
from os import read
from numpy.core.numeric import NaN
import pandas as pd
from pandas.core.frame import DataFrame
from requests.models import Response

from package.subpackage1.auth import DATA, AuthGooglemap
from package.subpackage1.time_count import time_end, time_start
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)
from package.subpackage1 import *
import numpy as np
import collections
radius = 300
CITY = 'Kaohsiung'

config = ConfigParser()
config.read('token.ini', encoding='utf8')
app_id = config['token']['id']
app_key = config['token']['key']
googlemaps_key = config['googlemaps-token']['key']
p = auth.AuthPTX(app_id, app_key)
g = auth.AuthGooglemap(googlemaps_key)

def main_2():
    while True:
        '''====================
        | 輸入資料
        ===================='''
        print(f'市區公車查詢系統！將為您找出附近 {radius} 公尺內可搭乘的公車站')
        # input_origins = input('我現在人在：')
        # input_destinations = input('我想要到：')
        input('Click to start')
        input_origins = '樹德'
        input_destinations = '高科燕巢'
        print()
        
        '''====================
        | 讀取所在地公車站資訊
        ===================='''
        response = getNearByStation(input_origins)
        if response['status_code'] == 200:
            origins = response['result']

        '''====================
        | 讀取目的地公車站資訊
        ===================='''
        response = getNearByStation(input_destinations)
        if response['status_code'] == 200:
            destinations = response['result']

        routes = set()
        result = list()
        result_dataframe = pd.DataFrame()
        for index, columns in destinations.iterrows():
            for _index, _columns in origins.iterrows():
                sameRoute = set(value['RouteName']['Zh_tw'] for value in _columns['Stops']) & set(value['RouteName']['Zh_tw'] for value in columns['Stops']) #|  會經過所在地與目的地的路線
                route = f'{_columns["StationID"]}, {columns["StationID"]}, {sameRoute}'
                
                if (sameRoute != set()) and (route not in routes):
                    routes.add(route)
                    getSchedule(_columns["StationID"], _columns["StationName"]['Zh_tw'], columns["StationName"]['Zh_tw'])
                    
                    originsEstimate = getEstimatedTimeOfArrival(_columns["StationID"]) #| 所在地附近公車站的預計到站資料
                    if len(originsEstimate.index) > 0:
                        bus = pd.DataFrame()
                        bus = originsEstimate[originsEstimate['RouteName'].apply(lambda x : x['Zh_tw']).isin(sameRoute)]

                        for _index, __columns in bus.iterrows():
                            if (True if 'Estimates' not in __columns.index else (type(__columns['Estimates']) == float)):
                                continue # 略過此步驟
                                # _dict = {
                                #     '公車路線': __columns['RouteName']['Zh_tw'], 
                                #     '出發站': _columns["StationName"]['Zh_tw'], 
                                #     '出發車站ID': _columns["StationID"], 
                                #     '目標站': columns["StationName"]['Zh_tw'], 
                                #     '目標車站ID': columns["StationID"]
                                # }
                                # new_row = pd.DataFrame(_dict, index=[0])
                                # result_dataframe = result_dataframe.append(new_row, ignore_index=True)

                            else:
                                for _ in __columns['Estimates']:
                                    _dict = {
                                        '車牌號碼': _["PlateNumb"], 
                                        '公車路線': __columns['RouteName']['Zh_tw'], 
                                        '出發站': _columns["StationName"]['Zh_tw'], 
                                        '出發車站ID': _columns["StationID"], 
                                        '預計到站時間': _["EstimateTime"], 
                                        # '預計到站時間': '{:g}'.format(_["EstimateTime"] / 60) + '分' if _["EstimateTime"] > 60  else f'{_["EstimateTime"]}秒', 
                                        '目標站': columns["StationName"]['Zh_tw'], 
                                        '目標車站ID': columns["StationID"]
                                    }
                                    new_row = pd.DataFrame(_dict, index=[0])
                                    result_dataframe = result_dataframe.append(new_row, ignore_index=True)
                    else:
                        #| 列數為 0，表示該站位無任何車輛停靠
                        pass
        # result_dataframe = result_dataframe.sort_values(['預計到站時間'])
        print(result_dataframe)
        try:
            result_dataframe.to_csv(f'csv/{input_origins} to {input_destinations}.csv', encoding='utf_8_sig')

        except PermissionError:
            print(f'沒有權限，csv匯出失敗，{input_origins} to {input_destinations}.csv 正在使用中')
            
        print(('====================分隔線====================\n\n'))




        continue
        for (di_, _) in enumerate(destinations['RouteNameList']):
            for (oi_, _) in enumerate(origins['RouteNameList']):
                '''====================
                | 允許搭乘的路線
                ===================='''
                sameRoute = set(origins['RouteNameList'][oi_]) & set(destinations['RouteNameList'][di_]) #|  會經過所在地與目的地的路線

                route = f'{origins["StationID"][oi_]}, {destinations["StationID"][di_]}, {sameRoute}'
                if (sameRoute != set()) and (route not in routes):
                    routes.add(route)
                    getSchedule(origins["StationID"][oi_], destinations["StationID"][di_])
                    # destinationsEstimate = getEstimatedTimeOfArrival(destinations["StationID"][di_]) #| 目的地附近公車站的預計到站資料


                    # print(originsEstimate['RouteName'].apply(lambda x : x['Zh_tw']))
                    '''====================
                    | 允許搭乘的車次
                    ===================='''
                    # bus = dict()
                    # for _, _row in originsEstimate.iterrows():
                    #     if _row['RouteName'] in sameRoute:
                    #         bus[_row['RouteName']] = list()
                    #         for _estimateTime in ([] if _row['EstimateTimes'] is None else _row['EstimateTimes']):
                    #             bus[_row['RouteName']].append({'PlateNumb':  _row['PlateNumb'], 'EstimateTime': _estimateTime})
                    
                    originsEstimate = getEstimatedTimeOfArrival(origins["StationID"][oi_]) #| 所在地附近公車站的預計到站資料
                    if len(originsEstimate.index) > 0:
                        bus = pd.DataFrame()
                        bus = originsEstimate[originsEstimate['RouteName'].apply(lambda x : x['Zh_tw']).isin(sameRoute)]

                        for _index, _columns in bus.iterrows():
                            if (True if 'Estimates' not in _columns.index else (type(_columns['Estimates']) == float)):
                                continue # 略過此步驟
                                # _dict = {
                                #     '公車路線': _columns['RouteName']['Zh_tw'], 
                                #     '出發站': origins["StationName"][oi_], 
                                #     '出發車站ID': origins["StationID"][oi_], 
                                #     '目標站': destinations["StationName"][di_], 
                                #     '目標車站ID': destinations["StationID"][di_]
                                # }
                                # new_row = pd.DataFrame(_dict, index=[0])
                                # result_dataframe = result_dataframe.append(new_row, ignore_index=True)

                            else:
                                for _ in _columns['Estimates']:
                                    _dict = {
                                        '車牌號碼': _["PlateNumb"], 
                                        '公車路線': _columns['RouteName']['Zh_tw'], 
                                        '出發站': origins["StationName"][oi_], 
                                        '出發車站ID': origins["StationID"][oi_], 
                                        '預計到站時間': '{:g}'.format(_["EstimateTime"] / 60) + '分' if _["EstimateTime"] > 60  else f'{_["EstimateTime"]}秒', 
                                        '目標站': destinations["StationName"][di_], 
                                        '目標車站ID': destinations["StationID"][di_]
                                    }
                                    new_row = pd.DataFrame(_dict, index=[0])
                                    result_dataframe = result_dataframe.append(new_row, ignore_index=True)
                    else:
                        #| 列數為 0，表示該站位無任何車輛停靠
                        pass
                        

                    # bus = dict()
                    # for _, _row in originsEstimate.iterrows():
                    #     _route = _row['RouteName']['Zh_tw']
                    #     if _route in sameRoute:
                    #         bus[_route] = list()
                    #         if _row['Estimates'] != NaN:
                    #             for _ in _row['Estimates']:
                    #                 _data = {
                    #                     'PlateNumb':  _['PlateNumb'], 
                    #                     'EstimateTime': _['EstimateTime']
                    #                 }
                    #                 bus[_route] = _data
                    
                    # # print(bus) 
                    # # bus = dict(zip(sameRoute, [time.get(_, {'PlateNumb': '', 'EstimateTime': None}) for _ in sameRoute]))
                    # list_ = list()
                    # for _key, _value in bus.items():
                        
                    #     if _value == list():
                    #         # list_.append(f'{_key} 無發車\n')
                    #         # new_row = pd.DataFrame({'公車路線': _key, '出發站': origins["StationName"][oi_], '抵達站': destinations["StationName"][di_]}, index=[0])
                    #         # result_dataframe = result_dataframe.append(new_row, ignore_index=True)
                    #         pass

                    #     else:
                    #         for _ in _value:
                    #             _dict = {
                    #                 '車牌號碼': _["PlateNumb"], 
                    #                 '公車路線': _key, 
                    #                 '出發站': origins["StationName"][oi_], 
                    #                 '出發車站ID': origins["StationID"][oi_], 
                    #                 '預計到站時間': '{:g}'.format(_["EstimateTime"] / 60) + '分' if _["EstimateTime"] > 60  else f'{_["EstimateTime"]}秒', 
                    #                 '目標站': destinations["StationName"][di_], 
                    #                 '目標車站ID': destinations["StationID"][oi_]
                    #             }
                    #             # list_.append(f'({_dict["車牌號碼"]}){_dict["公車路線"]}(預計到站：{_dict["預計到站時間"]} 分)\n')
                    #             new_row = pd.DataFrame(_dict, index=[0])
                    #             result_dataframe = result_dataframe.append(new_row, ignore_index=True)

                            
                    # list_ = list()
                    # for _key, _value in bus.items():
                        
                    #     if _value == list():
                    #         # list_.append(f'{_key} 無發車\n')
                    #         # new_row = pd.DataFrame({'公車路線': _key, '出發站': origins["StationName"][oi_], '抵達站': destinations["StationName"][di_]}, index=[0])
                    #         # result_dataframe = result_dataframe.append(new_row, ignore_index=True)
                    #         pass

                    #     else:
                    #         for _ in _value:
                    #             _dict = {
                    #                 '車牌號碼': _["PlateNumb"], 
                    #                 '公車路線': _key, 
                    #                 '出發站': origins["StationName"][oi_], 
                    #                 '出發車站ID': origins["StationID"][oi_], 
                    #                 '預計到站時間': '{:g}'.format(_["EstimateTime"] / 60) + '分' if _["EstimateTime"] > 60  else f'{_["EstimateTime"]}秒', 
                    #                 '目標站': destinations["StationName"][di_], 
                    #                 '目標車站ID': destinations["StationID"][oi_]
                    #             }
                    #             # list_.append(f'({_dict["車牌號碼"]}){_dict["公車路線"]}(預計到站：{_dict["預計到站時間"]} 分)\n')
                    #             new_row = pd.DataFrame(_dict, index=[0])
                    #             result_dataframe = result_dataframe.append(new_row, ignore_index=True)

                    # for _key, _value in bus.items():
                    #     if _value["EstimateTime"] is not None:
                    #         for _ in _value["EstimateTime"]:
                    #             list_.append(f'({_value["PlateNumb"]}){_key}(預計到站：{_ / 60} 分)\n')
                    #     else:
                    #         #| 空車路線
                    #         # list_.append(f'{_key} 無發車\n')
                    #         pass

                    # if len(list_) > 0:
                    #     message = f'你可以在{origins["StationID"][oi_]} {origins["StationName"][oi_]} 搭乘下列公車路線到 {destinations["StationName"][di_]}\n'
                    #     result.append(message + \
                    #         f'{"".join(list_)}\n')

                # try:
                # except Exception as e:
                #     print(destinations.loc[di_])
                #     pass

                # finally:
                #     try:
                #         origins.to_csv('csv/origins.csv', encoding='utf_8_sig')
                #         destinations.to_csv('csv/destinations.csv', encoding='utf_8_sig')
                #     except PermissionError:
                #         print("權限被拒")
        # if result == list():
        #     print('目前時間所在地附近的公車站沒有任何前往目的地附近的公車')
        # else:
        #     for _ in result:
        #         print(_)
        # result_dataframe.sort_values(by=['預計到站時間'])
        # result_dataframe = result_dataframe.groupby(['公車路線', '出發站', '抵達站']).apply(lambda x: [', '.join(list(x['預計到站時間']))]).apply(pd.Series)
        # result_dataframe = result_dataframe.groupby(['公車路線', '出發站', '目標站']).apply(lambda x: [', '.join(list(x['預計到站時間']))]).apply(pd.Series)
        # result_dataframe.columns = ['預計到站時間']
        print(result_dataframe)
        try:
            result_dataframe.to_csv(f'csv/{input_origins} to {input_destinations}.csv', encoding='utf_8_sig')

        except PermissionError:
            print(f'沒有權限，csv匯出失敗，{input_origins} to {input_destinations}.csv 正在使用中')
            
        print(('====================分隔線====================\n\n'))

def getNearByStation(address):
    r = g.get_geocode(address)
    if r['status_code'] == 200:
        location = r['result']
        params= {
            # '$top': 20, 
            '$spatialFilter': f'nearby({location["lat"]}, {location["lng"]}, {radius})', 
            '$format': 'JSON'
        }
        response = p.request('Station/NearBy', params)
        if response.status_code == 200:
            data = json.loads(response.content)
            #points = [g.distancematrix(address, f"{i['StationPosition']['PositionLat']},{i['StationPosition']['PositionLon']}") for i in data]
            # df =  = pd.DataFrame({
            #     # '組StationID': [i['StationGroupID'] if 'StationGroupID' in i else None for i in data], #有些縣市沒有提供組StationID
            #     'StationID': [i['StationID'] for i in data],
            #     'StationName': [i['StationName']['Zh_tw'] for i in data],
            #     'RouteNameList': [[j['RouteName']['Zh_tw'] for j in i['Stops']] for i in data]
            #     # 'RouteID': [[j['RouteID'] for j in i['Stops']] for i in data]
            # })
            df = pd.DataFrame(data)
            df.to_csv(f'csv/test/test.csv', encoding='utf_8_sig')
            r['result'] = df
            return r
            
        else:
            print(response.status_code)
    else:
        return r

'''====================
| 取得公車站預計到站資訊
===================='''
def getEstimatedTimeOfArrival(stationID, city=CITY):
    params= {
        # '$top': 20, 
        '$format': 'JSON'
    }
    response = p.request(f'EstimatedTimeOfArrival/City/{city}/PassThrough/Station/{stationID}', params)
    if response.status_code == 200:
        data = json.loads(response.content)
        df = pd.DataFrame(data)
        df.to_csv(f'csv/{stationID}.csv', encoding='utf_8_sig')
        return df
        
    else:
        print(response.status_code)

'''====================
| 取得公車站固定班表
===================='''
def getSchedule(stationID, origin, destination, city=CITY):
    print(origin)
    params= {
        '$format': 'JSON'
    }
    response = p.request(f'Schedule/City/{city}/PassThrough/Station/{stationID}', params)
    if response.status_code == 200:
        data = json.loads(response.content)
        df = pd.DataFrame()
        for ___index, ___value in enumerate(data):
            for __index, __value in enumerate(___value['Timetables']):
                if (__value['ServiceDay']['Monday'] and __value['ServiceDay']['Tuesday'] and __value['ServiceDay']['Wednesday'] and __value['ServiceDay']['Thursday']  and __value['ServiceDay']['Friday']):
                    _data = collections.OrderedDict()
                    
                    condition = False
                    for _index, _value in enumerate(__value['StopTimes']):
                        if (_value['StopName']['Zh_tw'] == origin):
                            condition = True
                            
                        if condition:
                            _data[_value['StopName']['Zh_tw']] = _value['ArrivalTime']

                        if (_value['StopName']['Zh_tw'] == destination):
                            condition = False
                    if condition == False:
                        df = df.append(_data, ignore_index=True)
                        print(df)
                        quit()
        df.to_csv(f'csv/test/{origin} to {destination}.csv', encoding='utf_8_sig')
        return df
        
    else:
        print(response.status_code)

'''====================
| 取得109行政區人口統計資料
===================='''
def getDemographicData():
    d = DATA()
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
        # '$top': 2,
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
                    latlng = f'{_["StationPosition"]["PositionLat"]},{_["StationPosition"]["PositionLon"]}'
                    response_ = dict() ; response_['status'] = 'OK'
                    # response_ = g.get_geocode_uselatlng(latlng)
                    time.sleep(0.021) # Geocoding API 有 50 QPS(每秒請求數)限制，因此在迴圈增加 21ms 延遲
                    if response_['status'] == 'OK':
                        _list.add(_stationName)

                    #     compound_code = response_['plus_code']['compound_code']
                        columns = {
                            'station_name': _stationName,
                            'latlng': latlng, 
                            # 'district': compound_code[compound_code.find('高雄市'):] #只取'高雄市'以後的字串
                        }
                        new_row = pd.DataFrame(columns, index=[0])
                        df = df.append(new_row, ignore_index=True)
                    else:
                        print(response_['status'])
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
    df = pd.read_csv('csv/公車站位.csv')
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

'''-------------------------------------------------'''
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['Taipei Sans TC Beta']

time_start()
getStationLocation()

# show()


time_end()