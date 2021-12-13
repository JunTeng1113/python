import auth
import configparser
import json
import pandas as pd

CITY = 'Kaohsiung'
def main():
    config = configparser.ConfigParser()
    config.read('config.ini')
    app_id = config['token']['id']
    app_key = config['token']['key']
    googlemaps_key = config['googlemaps-token']['key']
    global p 
    p = auth.AuthPTX(app_id, app_key)
    global g 
    g = auth.AuthGooglemap(googlemaps_key)

    while True:
        print(f'市區公車查詢系統！將為您找出附近 {radius} 公尺內可搭乘的公車站')
        input_origins = input('我現在人在：')
        input_destinations = input('我想要到：')
        origins = getNearByStation(input_origins)
        destinations = getNearByStation(input_destinations)
        #result = pd.merge(origins['行經路線'], destinations['行經路線'], how='inner')
        routes = set()
        result = list()
        for (index, key) in enumerate(destinations['行經路線']):
            for (i, k) in enumerate(origins['行經路線']):
                sameRoute = set(origins['行經路線'][i]) & set(destinations['行經路線'][index]) #會經過所在地與目的地的路線
                route = f'{origins["站位ID"][i]}, {destinations["站位ID"][index]}, {sameRoute}'
                # try:
                if True:
                    # if origins["組站位ID"][i] is not None:
                    #     route = f'{origins["組站位ID"][i]}, {destinations["組站位ID"][index]}'

                    # else:
                    #     route = f'{origins["站牌名稱"][i]}, {destinations["站牌名稱"][index]}, {destinations["行經路線"][index]}'
                    
                    if (sameRoute != set()) and (route not in routes):
                        routes.add(route)
                        allowRoutesName = list(sameRoute) #允許搭乘的公車路線

                        df = getEstimatedTimeOfArrival(CITY, destinations["站位ID"][index])
                        df.to_csv(f'csv/{destinations["站位ID"][index]}{destinations["站牌名稱"][index]}.csv', encoding='utf_8_sig')

                        df = getEstimatedTimeOfArrival(CITY, origins["站位ID"][i])
                        df.to_csv(f'csv/{origins["站位ID"][i]}{origins["站牌名稱"][i]}.csv', encoding='utf_8_sig')

                        

                        time = dict()
                        for _, _row in df.iterrows():
                            if _row['RouteName'] in allowRoutesName:
                                time[_row['RouteName']] = dict()
                                time[_row['RouteName']]['預計到站時間'] = _row['預計到站時間']
                                time[_row['RouteName']]['到站順序'] = _row['StopSequence']
                                time[_row['RouteName']]['方向'] = _row['Direction']
                                
                        allowRoutes = dict(zip(allowRoutesName, [time.get(_, {'預計到站時間': None, 'StopSequence': None, 'Direction': None}) for _ in allowRoutesName]))
                        
                        '''--------------------
                        | 刪除空車路線
                        --------------------'''
                        # for _key, _value in dict(allowRoutes).items():
                        #     if _value is None:
                        #         allowRoutes.pop(_key)
                        
                        
                        list_ = list()
                        for _key, _value in allowRoutes.items():
                            if _value["預計到站時間"] is not None:
                                for _ in _value["預計到站時間"]:
                                    list_.append(f'{_key}(預計到站：{_ / 60} 分)\n')
                            else:
                                # list_.append(f'{_key}(預計到站："" 分)\n')
                                pass

                        if len(list_) > 0:
                            message = f'你可以在 {origins["站位ID"][i]} {origins["站牌名稱"][i]} 搭乘下列公車路線到 {destinations["站牌名稱"][index]}\n'
                            result.append(message + \
                                f'{"".join(list_)}\n')

                # try:
                # except Exception as e:
                #     print(destinations.loc[index])
                #     pass

                # finally:
                #     try:
                #         origins.to_csv('csv/origins.csv', encoding='utf_8_sig')
                #         destinations.to_csv('csv/destinations.csv', encoding='utf_8_sig')
                #     except PermissionError:
                #         print("權限被拒")

        for i in result:
            print(i)
        print(('====================分隔線====================\n\n'))

radius = 500
def getNearByStation(address):
    location = g.get_geocode(address)
    params= {
        '$top': 20, 
        '$spatialFilter': f'nearby({location["lat"]}, {location["lng"]}, {radius})', 
        '$format': 'JSON'
    }
    response = p.request('Station/NearBy', params)
    if response.status_code == 200:
        data = json.loads(response.content)
        #points = [g.distancematrix(address, f"{i['StationPosition']['PositionLat']},{i['StationPosition']['PositionLon']}") for i in data]
        df = pd.DataFrame({
            # '組站位ID': [i['StationGroupID'] if 'StationGroupID' in i else None for i in data], #有些縣市沒有提供組站位ID
            '站位ID': [i['StationID'] for i in data],
            '站牌名稱': [i['StationName']['Zh_tw'] for i in data],
            '行經路線': [[j['RouteName']['Zh_tw'] for j in i['Stops']] for i in data]
            # 'RouteID': [[j['RouteID'] for j in i['Stops']] for i in data]
        })
        return df
        
    else:
        print(response.status_code)

def getEstimatedTimeOfArrival(city, stationID):
    params= {
        '$top': 20, 
        '$format': 'JSON'
    }
    response = p.request(f'EstimatedTimeOfArrival/City/{city}/PassThrough/Station/{stationID}', params)
    if response.status_code == 200:
        data = json.loads(response.content)
        #points = [g.distancematrix(address, f"{i['StationPosition']['PositionLat']},{i['StationPosition']['PositionLon']}") for i in data]
        df = pd.DataFrame({
            '預計到站時間': [([j['EstimateTime'] for j in i['Estimates']] if 'Estimates' in i else None) for i in data], #有些縣市沒有提供組站位ID
            'RouteName': [_['RouteName']['Zh_tw'] for _ in data],
            'StopSequence': [_['StopSequence'] for _ in data],
            'Direction': [_['Direction'] for _ in data],
            'StopStatus': [_['StopStatus'] for _ in data]
        }) 
        return df
        
    else:
        print(response.status_code)

main()