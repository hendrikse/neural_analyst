#!/usr/bin/env python
# A basic ZAP Python API example which spiders and scans a target URL

import time
from pprint import pprint
from zapv2 import ZAPv2
import json

target = 'http://0.0.0.0:32777/htmli_get.php'
apikey = 'None' # Change to match the API key set in ZAP, or use None if the API key is disabled
#
# By default ZAP API client will connect to port 8080
zap = ZAPv2(apikey=apikey, proxies={'http': 'http://localhost:8080', 'https': 'http://localhost:8080'})
# Use the line below if ZAP is not listening on port 8080, for example, if listening on port 8090
# zap = ZAPv2(apikey=apikey, proxies={'http': 'http://127.0.0.1:8090', 'https': 'http://127.0.0.1:8090'})

useProxyChain = False

core = zap.core

# Proxy a request to the target so that ZAP has something to deal with
print('Accessing target {}'.format(target))
test = zap.urlopen(target)

# Give the sites tree a chance to get updated
time.sleep(2)

# Spider
print('Spidering target {}'.format(target))
scanid = zap.spider.scan(target)
print(scanid)

# Give the Spider a chance to start
time.sleep(2)

# while (int(zap.spider.status(scanid)) < 100):
#     # Loop until the spider has finished
#     print('Spider progress %: {}'.format(zap.spider.status(scanid)))
#
# print ('Spider completed')

print ('Active Scanning target {}'.format(target))

scanid = zap.ascan.scan(target)

print('This is the scanid {}'.format(scanid))
while (int(zap.ascan.status(scanid)) < 100):
    # Loop until the scanner has finished
    print('Message: {}'.format(zap.core.message(id)))
    #print ('Scan progress %: {}'.format(zap.ascan.status(scanid)))
    time.sleep(10)

ids = zap.ascan.messages_ids(scanid)
print("Numbers of IDs: {}".format(len(ids)))


# print(ids)
# for id in ids:
    # file = open("data/train/0/" + id + ".txt", "w")
    # message = zap.core.message(id)
    # file.write(message["requestHeader"] + "\n")
    # file.write(message["requestBody"] + "\n")
    # file.write(message["responseHeader"] + "\n")
    # file.write(message["responseBody"])
    # print(zap.core.alerts(id))
    # file.close()
print ('Active Scan completed')

# Report the results
print ('Alerts: {}'.format(zap.ascan.alerts_ids(scanid)))

pprint('Enable all passive scanners -> ' +
        zap.pscan.enable_all_scanners())

ascan = zap.ascan

