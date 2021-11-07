import pyupbit
import pandas
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

plt.rcParams["figure.figsize"] = (12,6)
plt.rcParams["axes.formatter.limits"] = -10000, 10000

a="KRW-bora"

df = pyupbit.get_ohlcv(a)

w= 15 # 기준 이동평균일 
k= 3 # 기준 상수
 
#중심선 (MBB) : n일 이동평균선
df["mbb"]=df["close"].rolling(w).mean()
df["MA20_std"]=df["close"].rolling(w).std()
closedata = df["close"] 
delta = closedata.diff() 
 
#상한선 (UBB) : 중심선 + (표준편차 × K)
#하한선 (LBB) : 중심선 - (표준편차 × K)
df["ubb"]=df.apply(lambda x: x["mbb"]+k*x["MA20_std"],1)
df["lbb"]=df.apply(lambda x: x["mbb"]-k*x["MA20_std"],1)

# data = pyupbit.get_ohlcv(ticker=a)

ups, downs = delta.copy(), delta.copy() 
ups[ups < 0] = 0 
downs[downs > 0] = 0 

period = 7 
au = ups.ewm(com = period-1, min_periods = period).mean() 
ad = downs.abs().ewm(com = period-1, min_periods = period).mean() 

RS = au/ad 
RSI = pandas.Series(100 - (100/(1+RS))) 
df["RSI"]=RSI
# print(RSI)

print(df)

df.to_excel("band.xlsx")

df[["close","lbb"]].plot(secondary_y=["volume"])

plt.show()