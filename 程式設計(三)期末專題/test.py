import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

'''
提供公車站牌 dataframe 資料，輸出地圖
'''
def showMap(df):
    fig, ax = plt.subplots()
    ax.set_aspect('equal')

    town_shp = gpd.read_file('./mapdata202104280245/TOWN_MOI_1100415.shp', encoding='utf-8')
    town_shp[town_shp['COUNTYNAME']!='高雄市'].plot(ax=ax, color='gray')
    town_shp[town_shp['COUNTYNAME']=='高雄市'].plot(ax=ax)

    df = pd.read_csv('./data.csv', encoding='utf_8_sig')
    df = df[df['district'].str.contains('高雄市')] # 刪除高雄市以外的公車站牌
    
    plt.scatter(df['lng'], df['lat'], c='yellow', s=5, marker='.')
    plt.axis([120.1, 121.1, 22.4, 23.5])
    plt.show()

showMap(None)