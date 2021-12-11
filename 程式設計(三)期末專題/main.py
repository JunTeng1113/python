import auth
import configparser
import json
import pandas as pd

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
        print('Warning！！本系統不支援跨縣市！！')
        input_origins = input('我現在人在：')
        input_destinations = input('我想要到：')
        origins = getNearByStation(input_origins)
        destinations = getNearByStation(input_destinations)
        #result = pd.merge(origins['行經路線'], destinations['行經路線'], how='inner')
        routes = set()
        for (index, key) in enumerate(destinations['行經路線']):
            for (i, k) in enumerate(origins['行經路線']):
                if origins.get('組站位ID') is not None:
                    route = f'{origins["組站位ID"][i]}, {destinations["組站位ID"][index]}'
                    if (set(origins['行經路線'][i]) & set(destinations['行經路線'][index])) and (route not in routes):
                        routes.add(route)
                        print(f'你可以在 {origins["站牌名稱"][i]} 搭乘 {", ".join(set(origins["行經路線"][i]) & set(destinations["行經路線"][index]))} 到 {destinations["站牌名稱"][index]} ')
                else:
                    route = f'{origins["站牌名稱"][i]}, {destinations["站牌名稱"][index]}, {destinations["行經路線"][index]}'
                    if (set(origins['行經路線'][i]) & set(destinations['行經路線'][index])) and (route not in routes):
                        routes.add(route)
                        print(f'你可以在 {origins["站牌名稱"][i]} 搭乘 {", ".join(set(origins["行經路線"][i]) & set(destinations["行經路線"][index]))} 到 {destinations["站牌名稱"][index]} ')
        print(('====================分隔線===================='))


def getNearByStation(address):
    location = g.get_geocode(address)
    params= {
        '$top': 10, 
        '$spatialFilter': f'nearby({location["lat"]}, {location["lng"]}, 500)', 
        '$format': 'JSON'
    }
    response = p.request('Station', 'NearBy', params, city=False)
    if response.status_code == 200:
        data = json.loads(response.content)
        #points = [g.distancematrix(address, f"{i['StationPosition']['PositionLat']},{i['StationPosition']['PositionLon']}") for i in data]
        df = pd.DataFrame({
            #'組站位ID': [i['StationGroupID'] for i in data],
            '站位ID': [i['StationID'] for i in data],
            '站牌名稱': [i['StationName']['Zh_tw'] for i in data],
            '行經路線': [[j['RouteName']['Zh_tw'] for j in i['Stops']] for i in data]
        })
        #刪除重複站牌
        # df = df.drop_duplicates(subset=None, 
        #                     keep='first', 
        #                     inplace=False, 
        #                     ignore_index=True)
        return df
        
    else:
        print(response.status_code)

main()