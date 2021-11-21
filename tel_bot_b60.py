import pyupbit
import pandas
import pandas as pd
# import matplotlib.pyplot as plt
# import matplotlib as mpl
import numpy as np
import time
from datetime import datetime
import requests
import telepot

while True:

    # 원화 티커를 krw_tikers라는 변수에 저장합니다.
    krw_tickers = pyupbit.get_tickers(fiat = "KRW") 

    # pyupbit의 모듈을 사용했다면 업비트 사이트에서 자료를 받아오니 시간이 걸린다고 합니다.
    # 그래서 이렇게 타임 모듈을 사용해 0.1초 정도 쉬는 구간을 만들어 줘야 합니다.
    # 이런말이 있죠 모르면 외워
    time.sleep(0.1)
    # print(krw_tickers)
    target_tickers = [] # 자신이 원하는 티커들을 담을 리스트

    #원화 티커들을 for문을 통해 하나씩 가져옵니다 
    for i in krw_tickers: 

        # 가져온 티커의 현재가를 구합니다.
        df = pyupbit.get_ohlcv(i,interval='minute60',count=100)

        w = 15  # 기준 이동평균일
        k = 3  # 기준 상수

        #중심선 (MBB) : n일 이동평균선
        df["mbb"] = df["close"].rolling(w).mean()
        df["MA20_std"] = df["close"].rolling(w).std()
        # closedata = df["close"]
        # delta = closedata.diff()

        #상한선 (UBB) : 중심선 + (표준편차 × K)
        #하한선 (LBB) : 중심선 - (표준편차 × K)
        df["ubb"] = df.apply(lambda x: x["mbb"]+k*x["MA20_std"], 1)
        df["lbb"] = df.apply(lambda x: x["mbb"]-k*x["MA20_std"], 1)
        
        time.sleep(0.1)
        
        
        # if df["low"][-2] < df["lbb"][-2]:
        if df["ubb"][-3] < df["high"][-3]:
            if  df["ubb"][-2] < df["high"][-2]:
            #   if (df["open"][-3]+df["close"][-3])/2 < df["close"][-2]:
                # if ((df["close"][-3]/df["open"][-3])*100) > ((df["close"][-2]/df["open"][-2])*100):
                    # price = pyupbit.get_current_price(i)
                    # str_price = str(price)
                    # url = "https://www.upbit.com/exchange?code=CRIX.UPBIT."+i+"&tab=chart"
                    # #해당티커를 자신이 만든 리스트에 저장합니다.
                    # target_tickers.append(i + ":" + str_price + ":" + url)
             target_tickers.append(i)


    print(target_tickers)

    token = '2122111799:AAHqMghxAQJcsEnxgI5p8vlhKhkrFTDfGaQ'
    mc = '1771483621'

    bot = telepot.Bot(token)
    # bot.sendMessage(mc,(' '.join(target_tickers)))
    bot.sendMessage(mc,target_tickers)
    

    time.sleep(3600)