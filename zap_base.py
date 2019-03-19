#!/usr/bin/env python
# A basic ZAP Python API example which spiders and scans a target URL

import time
from pprint import pprint
from zapv2 import ZAPv2

target = 'http://localhost:32771'
apikey = 'None' # Change to match the API key set in ZAP, or use None if the API key is disabled
#
# By default ZAP API client will connect to port 8080
zap = ZAPv2(apikey=apikey, proxies={'http': 'http://localhost:8090', 'https': 'http://localhost:8090'})
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

while (int(zap.spider.status(scanid)) < 100):
    # Loop until the spider has finished
    print('Spider progress %: {}'.format(zap.spider.status(scanid)))
    time.sleep(2)

print ('Spider completed')


# Enable all passive scanners (it's possible to do a more specific policy by
# setting needed scan ID: Use zap.pscan.scanners() to list all passive scanner
# IDs, then use zap.scan.enable_scanners(ids) to enable what you want
pprint('Enable all passive scanners -> ' + zap.pscan.enable_all_scanners())
while (int(zap.pscan.records_to_scan) > 0):
      print ('Records to passive scan : {}'.format(zap.pscan.records_to_scan))
      time.sleep(2)

print ('Passive Scan completed')

print ('Active Scanning target {}'.format(target))
scanid = zap.ascan.scan(target)
while (int(zap.ascan.status(scanid)) < 100):
    # Loop until the scanner has finished
    print ('Scan progress %: {}'.format(zap.ascan.status(scanid)))
    print(zap.ascan.scan())
    time.sleep(10)

ids = zap.ascan.messages_ids(scanid)
print("Numbers of IDs: {}".format(len(ids)))

file = open("testfile.json","w")
for id in ids:
    file.write(str(zap.core.message(id)) + "\n")
file.close()
print ('Active Scan completed')

# Report the results
print ('Hosts: {}'.format(', '.join(zap.core.hosts)))
print ('Alerts: ')
pprint (zap.core.alert(scanid))