import time
import datetime
# day = time.strftime("%Y%m%d",time.localtime(time.time()))
# day_s = time.strptime(day+'-0:0:0','%Y%m%d-%H:%M:%S')
# day_e = time.strptime(str(int(day)+1)+'-0:0:0','%Y%m%d-%H:%M:%S')
# print day_s
# print day_e
day_e = datetime.date.today()
print day_e

def is_today(t):
    day_e = datetime.date.today()
    day_s = day_e+datetime.timedelta(-1)
    day_s = time.strptime(str(day_s)+'-0:0:0','%Y-%m-%d-%H:%M:%S')
    day_e = time.strptime(str(day_e)+'-0:0:0','%Y-%m-%d-%H:%M:%S')
    day_s = time.mktime(day_s)
    day_e = time.mktime(day_e)
    return t > day_s and t <day_e


