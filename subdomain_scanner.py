#!/usr/bin/python

###################################################
#######    THREADED SUBDOMAIN SCANNER    ##########
#                                                 #
# Usage: subdomain_scanner [-t #threads] -d domain #
#                                                 #
# Example: subdomain_scanner -t 16 -d yahoo.com    #
#                                                 #
#           Author: Josh Rabinowitz               #
###################################################

import argparse
import Queue
import requests as req
import sys
import threading
import time

start = time.time()

class myThread (threading.Thread):
    def __init__(self, threadID, name, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q
    def run(self):
        process_subdomain(self.name, self.q)
        
def process_subdomain(threadName, q):
    while not exitFlag:
        queueLock.acquire()
        if not workQueue.empty():
            subdomain = q.get()
            queueLock.release()
            url = subdomain+'.'+domain
            display_response('http://'+url)
            display_response('https://'+url)
        else:
            queueLock.release()
        time.sleep(1)

def display_response(url):
    try:
        resp = req.get(url, allow_redirects=False, timeout=5)
        status = str(resp.status_code)
        print('{:.<40s}{:.>40s}'.format(url,status))
    except:
        status = '[***]'
        print('{:.<40s}{:.>40s}'.format(url,status))

###**** MAIN: ****###
parser = argparse.ArgumentParser(description='A quick tool for enumerating subdomains')

parser.add_argument('-t','--threads',type=int,dest='num_threads',default=4,help='Number of threads to use (Default is 4, Max is 16)')
parser.add_argument('-d','--domain',dest='domain',required=True,help='Domain to enumerate')
args = parser.parse_args()
domain = args.domain
num_threads = args.num_threads

if (num_threads > 16):
    print("[*] Maximum thread count is 16!")
    sys.exit(1)

threadList = []
for i in range(1,num_threads+1):
    threadList.append('Thread-%d' %i)
#Populate list w/top common subdomain names
subdomain_list = ['www', 'mail', 'remote', 'blog', 'webmail', 'server', 'ns1', 'ns2', 'smtp', 'secure',
                  'vpn', 'm', 'shop', 'ftp', 'mail2', 'test', 'portal', 'ns', 'ww1', 'host', 'support',
                  'dev', 'web', 'bbs', 'ww42', 'mx', 'email', 'cloud', '1', 'mail1', '2', 'forum', 'owa',
                  'www2', 'gw', 'admin', 'store', 'mx1', 'cdn', 'api', 'exchange', 'app', 'gov', 'public',
                  'shopping','resources','sites','view','ldap','business','english','code','checkout','pages',
                  'student','downloads','games','dashboard','calendar','book','file','pay','update','domains',
                  'contact','sun','res']


queueLock = threading.Lock()
workQueue = Queue.Queue(100)
threads = []
threadID = 1
exitFlag = 0
dash = '-'*82
print("")
print("\t\tINITIALIZING SCAN . . .")
print("")
print(" - Domain to scan: %s" %domain)
print(" - Threads used: %d" %num_threads)
print(" - ('***' indicates connection refused or timed out)")
print("")
print(dash)
print('{:<40s}{:>40s}'.format('SUBDOMAIN','RESPONSE CODE'))
print(dash)

# Create new threads
for tName in threadList:
    thread = myThread(threadID, tName, workQueue)
    thread.start()
    threads.append(thread)
    threadID += 1

# Fill the queue
queueLock.acquire()
for word in subdomain_list:
    workQueue.put(word)
queueLock.release()

# Wait for queue to empty
while not workQueue.empty():
    pass

# Notify threads it's time to exit
exitFlag = 1

# Wait for all threads to complete
for t in threads:
    t.join()

end = time.time()
print("")
print("Time elapsed: "+str(end - start))
print("")
