from hashlib import sha1
import hmac
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
import base64
from requests import request
import json

app_id = '5827be7a93e04190a20003d4dc00a26f'
app_key = 'ShHsxWHX9b9Jfz_rUghl-vRwvK8'

class Auth():

    def __init__(self, app_id, app_key):
        self.app_id = app_id
        self.app_key = app_key

    def get_auth_header(self):
        xdate = format_date_time(mktime(datetime.now().timetuple()))
        hashed = hmac.new(self.app_key.encode('utf8'), ('x-date: ' + xdate).encode('utf8'), sha1)
        signature = base64.b64encode(hashed.digest()).decode()

        authorization = 'hmac username="' + self.app_id + '", ' + \
                        'algorithm="hmac-sha1", ' + \
                        'headers="x-date", ' + \
                        'signature="' + signature + '"'
        return {
            'Authorization': authorization,
            'x-date': format_date_time(mktime(datetime.now().timetuple())),
            'Accept - Encoding': 'gzip'
        }
        
while True:
    i_StationName = input("請輸入車站名稱(例如：田中)：")
    if __name__ == '__main__':
        a = Auth(app_id, app_key)

        # 取得指定車站資料
        response = request('get', 'https://ptx.transportdata.tw/MOTC/v2/Rail/TRA/Station?$format=JSON', headers= a.get_auth_header())
        if response.status_code == 200:
            data = json.loads(response.content)
            station_name = dict(zip([i['StationName']['Zh_tw'] for i in data], data))
            

            # 取得指定車站即將到站車次
            response_station = request('get', f"https://ptx.transportdata.tw/MOTC/v2/Rail/TRA/LiveBoard/Station/{station_name[i_StationName]['StationID']}?$format=JSON", headers= a.get_auth_header())
            if response_station.status_code == 200:
                data = json.loads(response_station.content)


                # 取得車次誤點情況(當前位置)
                response_train = request('get', f"https://ptx.transportdata.tw/MOTC/v2/Rail/TRA/LiveTrainDelay?$format=JSON", headers= a.get_auth_header())
                if response_train.status_code == 200:
                    data_train = json.loads(response_train.content)
                    train = dict(zip([i['TrainNo'] for i in data_train], data_train))
                    # print(train)
                else:
                    print("Train Error")

                print(f">>> 即將抵達 {station_name[i_StationName]['StationName']['Zh_tw']} 的列車 <<<")
                for d in data:
                    # 取得列車到站時間
                    response_trainNo = request('get', f"https://ptx.transportdata.tw/MOTC/v2/Rail/TRA/DailyTimetable/Today/TrainNo/{d['TrainNo']}?$format=JSON", headers= a.get_auth_header())
                    if response_trainNo.status_code == 200:
                        data_trainNo = json.loads(response_trainNo.content)
                        station_info = dict(zip([i['StationName']['Zh_tw'] for i in data_trainNo[0]['StopTimes']], data_trainNo[0]['StopTimes']))
                    else:
                        print("Train Error")

                    direction = '北上' if d['Direction'] == 0 else '南下'
                    print(f"車次：{d['TrainNo']}，方向：{direction}，車種：{d['TrainTypeName']['Zh_tw']}，抵達時間：{station_info[i_StationName]['ArrivalTime']}，" \
                        + f"誤點：{train[d['TrainNo']]['DelayTime']} 分鐘，終點站：{d['EndingStationName']['Zh_tw']}，目前位置：{train[d['TrainNo']]['StationName']['Zh_tw']}>>")
                print()
            else:
                print(response_station.status_code)
        else:
            print(response.status_code)

