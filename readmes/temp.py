import datetime

now = datetime.datetime.now()
now_str = now.strftime("%d%m%Y")
print(now_str)

date_str = "24052025"
waktu = datetime.datetime.strptime(date_str, "%d%m%Y")
print(waktu)

# if waktu in holiday:
dt = waktu - datetime.timedelta(days=2)
print(dt)

"""
1. kalau sekarang = tanggal holiday:
    maka ...
2. kalau sekarang != tanggal holiday:
    maka ...
3. dsb ...
"""