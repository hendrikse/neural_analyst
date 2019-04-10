import json
import os
import csv
from bs4 import BeautifulSoup

FOLDER_NAME = "data/test"
BENIGN = "/0"
VULNERABILITY = "/1"
print("Reading data from folder...{}".format(FOLDER_NAME))

def html_preprocess(htmlBody):
    htmlBody = htmlBody.lower()
    clean_text = BeautifulSoup(htmlBody, "html.parser")
    if clean_text.body:
        clean_text = clean_text.body
    return clean_text.text

def response_body_parser(responseBody):
    if len(responseBody) != 0:
        if isinstance(responseBody, str):
            return html_preprocess(responseBody)
        else:
            return json.dumps(raw_response_body)
    else:
        return " "


def one_liner(multiple_lines_str):
    return multiple_lines_str.replace('\n', ' ').replace('\r', ' ')

with open("zap_data.csv", "w") as csv_data_file:
    fieldnames = ['vul', 'content']
    writer = csv.DictWriter(csv_data_file, fieldnames=fieldnames)
    writer.writeheader()
    for filename in os.listdir(FOLDER_NAME + '/0'):
        with open(FOLDER_NAME + BENIGN + "/" + filename, "r") as file:
            content = json.loads(file.read())
            content_req_header = content['requestHeader']
            content_req_body = content['requestBody']
            content_req_body = response_body_parser(content_req_body)
            print(content_req_body)
            content_resp_header = content['responseHeader']
            raw_response_body = content["responseBody"]
            print(type(raw_response_body))
            content_resp_body = response_body_parser(raw_response_body)
            print(content_resp_body)
            print(filename)
            content = content_req_header + content_req_body + content_resp_header + str(content_resp_body)
            content = one_liner(content)
            writer.writerow({'vul': 0, 'content': content})

    for filename in os.listdir(FOLDER_NAME + '/1'):
        with open(FOLDER_NAME + VULNERABILITY + "/" + filename, "r") as file:
            content = json.loads(file.read())
            content_req_header = content['requestHeader']
            content_req_body = content['requestBody']
            content_req_body = response_body_parser(content_req_body)
            print(content_req_body)
            content_resp_header = content['responseHeader']
            raw_response_body = content["responseBody"]
            print(type(raw_response_body))
            content_resp_body = response_body_parser(raw_response_body)
            print(content_resp_body)
            print(filename)
            content = content_req_header + content_req_body + content_resp_header + str(content_resp_body)
            content = one_liner(content)
            writer.writerow({'vul': 0, 'content': content})