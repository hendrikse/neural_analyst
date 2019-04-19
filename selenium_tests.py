import unittest
from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
import time
from pprint import pprint
from zapv2 import ZAPv2

SELENIUM_HUB_ADDRESS = 'http://0.0.0.0:32781/wd/hub'
APIKEY = 'None' # Change to match the API key set in ZAP
TARGET_ADRESS = "http://172.17.0.4"


# OWASP A1 - Injection
HTML_INJECTION_REFLECTED_GET = '/htmli_get.php'
HTML_INJECTION_REFLECTED_POST = '/htmli_post.php'
HTML_INJECTION_REFLECTED_URL = '/htmli_current_url.php'
HTML_INJECTION_STORED_BLOG = '/htmli_stored.php'
IFRAME_INJECTION = '/iframei.php'
LDAP_INJECTION = ''
MAIL_HEADER_INJECTION =''
OS_COMMAND_INJECTION = ''
OS_COMMAND_INJECTION_BLIND = ''
PHP_CODE_INJECTION = ''

# set zed attack proxy
zap = ZAPv2(apikey=APIKEY)
# Use the line below if ZAP is not listening on port 8080, for example, if listening on port 8090
# zap = ZAPv2(apikey=apikey, proxies={'http': 'http://127.0.0.1:8090', 'https': 'http://127.0.0.1:8090'})


# Set zap proxy with defined docker ip address
PROXY_ADDRESS = "172.17.0.6:8080"
proxy = Proxy()
proxy.proxy_type = ProxyType.MANUAL
proxy.http_proxy = PROXY_ADDRESS
proxy.ssl_proxy = PROXY_ADDRESS

# set desired capabilities for firefox client
capabilities = webdriver.DesiredCapabilities.FIREFOX
proxy.add_to_capabilities(capabilities)

driver = webdriver.Remote(command_executor=SELENIUM_HUB_ADDRESS, desired_capabilities=capabilities)

def login_bwapp(target):
    driver.get(target + '/login.php')
    driver.find_element_by_id("login").send_keys("bee")
    driver.find_element_by_id("password").send_keys("bug")
    driver.find_element_by_name("form").click()



def request_target(self, target):
    # Proxy a request to the target so that ZAP has something to deal with
    print('Accessing target {}'.format(target))
    zap.urlopen(target)
    # Give the sites tree a chance to get updated
    time.sleep(2)

def start_spider(self, target):
    print('Spidering target {}'.format(target))
    scanid = zap.spider.scan(target)
    # Give the Spider a chance to start
    time.sleep(2)
    while (int(zap.spider.status(scanid)) < 100):
        # Loop until the spider has finished
        print('Spider progress %: {}'.format(zap.spider.status(scanid)))
        time.sleep(2)

    print('Spider completed')

def wait_for_passive_scan_to_complete():
    while (int(zap.pscan.records_to_scan) > 0):
        print('Records to passive scan : {}'.format(zap.pscan.records_to_scan))
        time.sleep(2)

    print('Passive Scan completed')

def start_ascan(self, target):
    print('Active Scanning target {}'.format(target))
    scanid = zap.ascan.scan(target)
    while (int(zap.ascan.status(scanid)) < 100):
        # Loop until the scanner has finished
        print('Scan progress %: {}'.format(zap.ascan.status(scanid)))
        time.sleep(5)

    print('Active Scan completed')

def get_scan_alerts():
    # Report the results
    print('Hosts: {}'.format(', '.join(zap.core.hosts)))
    print('Alerts: ')
    pprint(zap.core.alerts())

def get_request_message(self, id):
    # return the request messages from a certain request
    message = zap.core.message(id)
    req_message = message['requestHeader'] + '\n' + message['requestBody']
    return req_message

def get_response_message(self, id):
    # return the response messages from a certain request
    message = zap.core.message(id)
    resp_message = message['responseHeader'] + '\n' + message['responseBody']
    return resp_message

driver.get(TARGET_ADRESS)
if "Login" in driver.title:
    login_bwapp(TARGET_ADRESS)

driver.get(TARGET_ADRESS + '/htmli_get.php')
driver.find_element_by_id("firstname").send_keys("Bee")
driver.find_element_by_id("lastname").send_keys("Bug")
driver.find_element_by_name("form").click()

wait_for_passive_scan_to_complete()
print(zap.core.messages())
driver.close()


# class GoogleTestCase(unittest.TestCase):
#
#     def setUp(self):
#         self.browser = webdriver.Firefox()
#         self.addCleanup(self.browser.quit)
#
#     def testPageTitle(self):
#         self.browser.get('http://www.google.com')
#         self.assertIn('Google', self.browser.title)
#
#
# if __name__ == '__main__':
#     unittest.main(verbosity=2)

# zapProxy = "172.17.0.6:8080"
# proxy = Proxy({
#     'proxyType': ProxyType.MANUAL,
#     'httpProxy': zapProxy,
#     'sslProxy': zapProxy,
#     'fpProxy': zapProxy,
#     'noProxy': ''
# })
#
# driver = webdriver.Remote(
#     proxy = proxy,
#     command_executor='http://0.0.0.0:32779/wd/hub',
#     desired_capabilities=webdriver.DesiredCapabilities.FIREFOX
# )
#
# driver.get("http://172.17.0.4/ba_captcha_bypass.php")
# print(driver.title)
# driver.close()


# set chrome options
#chrome_options = ChromeOptions()
#chrome_options.add_argument("--ignore-certificate-errors")

# set proxy

def get_html_by_webdirver(url, proxies = ''):
    html = None
    try:

        driver = webdriver.PhantomJS()

        if proxies:
            proxy=webdriver.Proxy()
            proxy.proxy_type=ProxyType.MANUAL
            proxy.http_proxy= proxies  #'220.248.229.45:3128'
            #????????webdriver.DesiredCapabilities.PHANTOMJS?
            proxy.add_to_capabilities(webdriver.DesiredCapabilities.PHANTOMJS)
            driver.start_session(webdriver.DesiredCapabilities.PHANTOMJS)

        driver.get(url)
        html = driver.page_source
        # driver.save_screenshot('1.png')   #????
        driver.close()
    except Exception as e:
        return e
    return html and len(html) < 1024 * 1024 and html or None