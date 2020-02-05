import time

VERSION = (1,0,0)

def get_time():
   #Timestamp tick '1580182705.12'
   return time.time()

def format_clocktime_only(t):
   # 0: year
   # 1: month
   # 2: day
   # 3: hours
   # 4: minutes
   # 5: second
   ttuple = time.localtime(t)
   return "{}:{}:{}".format(ttuple[3], ttuple[4],ttuple[5]) 

def format_full_text(t):
   #return 'Mon Jan 27 22:37:24 2020'
   return time.asctime(time.localtime(t))

