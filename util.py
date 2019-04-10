import json

from bs4 import BeautifulSoup

def html_preprocess(htmlBody):
    htmlBody = htmlBody.lower()
    cleantext = BeautifulSoup(htmlBody, "html.parser")
    cleantext = cleantext.text
    return cleantext

def one_liner(multiple_lines_str):
    return multiple_lines_str.replace('\n', ' ').replace('\r', ' ')

data_path = 'testfile.txt'
counter = 0
with open(data_path) as fp:
    for line in fp:
        line = json.loads(line)
        responseBody = line["message"]["responseBody"]
        responseBodyText = html_preprocess(responseBody)

        responseHeader = line["message"]["responseHeader"]

        responseMessage = one_liner(responseHeader + responseBodyText)
        responseMessage = ' '.join(responseMessage.split())

        requestBody = line["message"]["requestBody"]
        requestHeader = line["message"]["requestHeader"]

        requestMessage = one_liner(requestHeader + requestBody)
        requestMessage = ' '.join(requestHeader.split())

        print(requestMessage + ' ' + responseMessage)

fp.close()

# 1. JSON lesen und tokenizen
# 2. RTT hinschreiben
# 3. resp.ResponseBody
# 3.a BeautifulSoup
# 3.b Buchstaben in kleinbuchstaben umwandeln
# 3.c URL-Normalisierung
###### Unbedingt NLTK-Library verwenden

#html_doc = html_doc.replace('\n', ' ').replace('\r', ' ')
#html_doc = html_doc.lower()



#cleantext = BeautifulSoup(html_doc, "html.parser")
#cleantext = cleantext.text


#print(cleantext)



