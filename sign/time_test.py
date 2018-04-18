import time

now_time = time.time()
print('current time:' + str(now_time))
otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now_time))
print('time format:' + str(otherStyleTime))