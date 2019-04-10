#!/usr/bin/env python
# A basic ZAP Python API example which spiders and scans a target URL

from zapv2 import ZAPv2
import json
import time
import csv
from urllib.parse import urlparse, quote
from bs4 import BeautifulSoup
from string import Template
# Change to scan targeting web application by url
TARGET = 'http://0.0.0.0:32779'
# By default ZAP API client will connect to port 8080
PROXY_ADDRESS = 'http://127.0.0.1:8080/'
# Change to match the API key set in ZAP, or use None if the API key is disabled
API_KEY = 'ee2remb6f90fa095sne3mop3h7'

zap = ZAPv2(apikey=API_KEY, proxies={'http': PROXY_ADDRESS, 'https': PROXY_ADDRESS})


def pscan():
    # Proxy a request to the target so that ZAP has something to deal with
    while int(zap.pscan.records_to_scan) > 0:
        print('Records to passive scan : {}'.format(zap.pscan.records_to_scan))
        time.sleep(2)
    print('Passive Scan completed')


def ascan():
    print('Active Scanning target {}'.format(TARGET))

    scanid = zap.ascan.scan(TARGET)

    print('This is the scanid {}'.format(scanid))
    while int(zap.ascan.status(scanid)) < 100:
        # Loop until the scanner has finished
        print("scanning...")
        # print ('Scan progress %: {}'.format(zap.ascan.status(scanid)))
        time.sleep(1)


def get_messages():
    messages = zap.core.messages(TARGET)
    return messages

def get_url_from_req_header(req_header):
    request_line = req_header.split('\r\n')
    request_line = request_line[0]
    request_line = request_line.split(' ')
    url = request_line[1]
    parsed = urlparse(url)
    #request_line[1] = parsed
    return parsed.netloc + parsed.path

def parse_response_body(response_body):
    # response_body.lower().replace('\n', ' ').replace('\r', ' ')
    # try:
    #     clean_text = BeautifulSoup(response_body, "html.parser")
    #     if clean_text:
    #         if clean_text.body:
    #             clean_text = clean_text.body
    #         return clean_text
    #     else:
    #         return response_body
    # except:
        return response_body.lower().replace('\n', ' ').replace('\r', ' ')

def messages_to_json_file(messages):
    data = {}
    for message in messages:
        message_content = {
            'messageId': message['id'],
            'requestHeader': parse_req_header(message['requestHeader']),
            'requestBody': message['requestBody'],
            'responseHeader': remove_multilines(message['responseHeader']),
            'responseBody': parse_response_body(message['responseBody']),
            'attacked': 0
        }
        message_id = int(message['id'])
        # todo eventuell besser wenn es mit gehashter URL geordnet wird, sodass man die differenz bilden kann => schneller und allgemeingültiger
        # ODER mit selenium die url ansprechen und differenz bilden, eventuell direkter Pool besser, da der ja existieren sollte
        url_hash = hash(get_url_from_req_header(message['requestHeader']))
        data[message_id] = message_content

    alert_ids = get_zap_alerts()
    for alert_id in alert_ids:
        data[int(alert_id)]['attacked'] = 1

    with open("data/test/0/jenkins_scan_time_" + str(time.time()) + ".json", "w") as file:
        file.write(json.dumps(data))
        file.close()
    return data


def remove_multilines(multilines):
    return multilines.replace('\r\n', ' ')


def json_to_csv(json_data, csv_file_path):
    # open a csv file to write content to it
    csv_file = open(csv_file_path, 'w')
    csv_writer = csv.writer(csv_file)
    count = 0

    for key, value in json_data.items():
        if count == 0:  # header row
            csv_writer.writerow(value.keys())
            count += 1
        csv_writer.writerow(value.values())  # values row


def parse_req_header(req_header):
    request_line = req_header.split('\n')
    request_line = request_line[0]
    # request_line = request_line.split(' ')
    # url = request_line[1]
    # parsed = urlparse(url)
    # request_line[1] = parsed
    # return ' '.join(request_line)
    return request_line


def get_zap_alerts():
    alerts = zap.core.alerts(TARGET)
    ids = []
    for alert in alerts:
        ids.append(alert['messageId'])
    return ids

def hash_url(url):
    return hash(url)

def generate_syntethic_data(data):
    with open('data/xss_example.txt', 'r') as f:
        message = json.load(f)
    template = message['responseBody']
    attacks = open("data/xss-payload-list.txt", "r")
    counter = 0
    for attack in attacks:
        message_id = hash(attack)
        message['responseBody'] = Template(template).substitute(attack_response=attack,
                                                                attack_request=quote(attack))

        message_content = {
            'messageId': message_id,
            'requestHeader': message['requestHeader'],
            'requestBody': message['requestBody'],
            'responseHeader': remove_multilines(message['responseHeader']),
            'responseBody': parse_response_body(message['responseBody']),
            'attacked': 1
        }
        data[message_id] = message_content
        print(message_id)
        print(data[message_id])
        counter += 1
    print(counter)
    attacks.close()
    return data

messages = get_messages()
data = messages_to_json_file(messages)
data = generate_syntethic_data(data)
json_to_csv(data, "data/test.csv")
# ids = zap.ascan.messages_ids(scanid)

# for id in ids:
# file = open("data/test/1/" + id + ".txt", "w")
# message = zap.core.message(id)
# file.write(message["requestHeader"] + "\n")
# file.write(message["requestBody"] + "\n")
# file.write(message["responseHeader"] + "\n")
# file.write(message["responseBody"])
# print(zap.core.alerts(id))
# file.close()


# print('Active Scanning target {}'.format(target))
# scanid = zap.ascan.scan(target)
# while (int(zap.ascan.status(scanid)) < 100):
# # Loop until the scanner has finished
#       print('Scan progress %: {}'.format(zap.ascan.status(scanid)))
#       time.sleep(5)
#
# print('Active Scan completed')
# file = open("alert_list_1721704.txt", "w")
# alerts = zap.core.alerts(target)
# for alert in alerts:
#       file.write(json.dumps(alert) + "\n")

# file.close()
#
#
# array = []
#
# with open("alert_list_1721704.txt", "r") as ins:
#     for line in ins:
#           alert = json.loads(line)
#           array.append(int(alert['messageId']))
# print(len(array))
#
# import os
# l=os.listdir('data/test/0/')
# li=[int(x.split('.')[0]) for x in l]
# print(len(li))
# i = 0
# for id in li:
#       if id in array:
#             i+= 1
#             os.remove("data/test/0/" + str(id) + ".txt")
# print("{} files Removed!".format(i))
# print(i)


# i = 0
# for id in array:
#       print('open {}'.format(i))
#       file = open("data/test/1/{}".format(i) + ".txt", "w")
#       message = zap.core.message(id)
#       json.dump(message, file)
#       file.close()
#       i += 1
