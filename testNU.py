import pyupbit

access = "hUU2UoxxBams2xitpRoMSCSPIXlX2jwM8c6AyNnx"          # 본인 값으로 변경
secret = "tS3MjPpdexOcuadKaSYyRADCQcgNFMfj9aiDw1KJ"          # 본인 값으로 변경
upbit = pyupbit.Upbit(access, secret)

print(upbit.get_balance("KRW-NU"))     # KRW-XRP 조회
print(upbit.get_balance("KRW"))         # 보유 현금 조회
