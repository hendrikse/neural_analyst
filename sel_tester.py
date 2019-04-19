from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# Selenium hub address
SELENIUM_HUB_ADDRESS = 'http://0.0.0.0:4444/wd/hub'

# Target address
TARGET_ADDRESS = 'http:/172.17.0.2'


# Set zap proxy with defined docker ip address
PROXY_ADDRESS = "172.17.0.4:8090" # should be changed in order to not use ip addresses
proxy = Proxy()
proxy.proxy_type = ProxyType.MANUAL
proxy.http_proxy = PROXY_ADDRESS
proxy.ssl_proxy = PROXY_ADDRESS



# set desired capabilities for firefox client
capabilities = webdriver.DesiredCapabilities.FIREFOX
proxy.add_to_capabilities(capabilities)


firefox = webdriver.Remote(keep_alive = True,
          command_executor=SELENIUM_HUB_ADDRESS,
          desired_capabilities=capabilities)
try:
    firefox.get(TARGET_ADDRESS)
    print(firefox.title)
except:
    print("error")
    firefox.quit()
firefox.quit()


