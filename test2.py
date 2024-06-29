import time

current_time= time.localtime()

year = current_time.tm_year
month = current_time.tm_mon
day = current_time.tm_mday
print(year)
print(month)
print(day)