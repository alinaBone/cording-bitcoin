import pyupbit
import pandas
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import time

# plt.rcParams["figure.figsize"] = (12,6)
# plt.rcParams["axes.formatter.limits"] = -10000, 10000

# 원화 티커를 krw_tikers라는 변수에 저장합니다.
krw_tickers = pyupbit.get_tickers(fiat = "KRW") 

# pyupbit의 모듈을 사용했다면 업비트 사이트에서 자료를 받아오니 시간이 걸린다고 합니다.
# 그래서 이렇게 타임 모듈을 사용해 0.1초 정도 쉬는 구간을 만들어 줘야 합니다.
# 이런말이 있죠 모르면 외워
time.sleep(0.1)

target_tickers = [] # 자신이 원하는 티커들을 담을 리스트

#원화 티커들을 for문을 통해 하나씩 가져옵니다 
for i in krw_tickers: 

    # 가져온 티커의 현재가를 구합니다.
    df = pyupbit.get_ohlcv(i,count=15)

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

    # 티커의 현재가격이 1000초과 5000미만이면
    # if df["low"][-1] < df["lbb"][-1]:
    if df["lbb"][-1] > df["low"][-1]:

        #해당티커를 자신이 만든 리스트에 저장합니다.
        target_tickers.append(i)

print(target_tickers)



# # data = pyupbit.get_ohlcv(ticker=a)

# ups, downs = delta.copy(), delta.copy() 
# ups[ups < 0] = 0 
# downs[downs > 0] = 0 

# period = 7 
# au = ups.ewm(com = period-1, min_periods = period).mean() 
# ad = downs.abs().ewm(com = period-1, min_periods = period).mean() 

# RS = au/ad 
# RSI = pandas.Series(100 - (100/(1+RS))) 
# df["RSI"]=RSI
# # print(RSI)

# print(df["lbb"],df["close"])

# df.to_excel("band.xlsx")

# df[["close","lbb"]].plot(secondary_y=["volume"])

# plt.show()