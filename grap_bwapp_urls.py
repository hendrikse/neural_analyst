from selenium import webdriver

driver = webdriver.Firefox()

def login_bwapp(target):
    driver.get(target + '/login.php')
    driver.find_element_by_id("login").send_keys("bee")
    driver.find_element_by_id("password").send_keys("bug")
    driver.find_element_by_name("form").click()

TARGET_ADRESS = "http://0.0.0.0:32777"
login_bwapp(TARGET_ADRESS)
driver.get(TARGET_ADRESS)

driver.find_element_by_id('select_portal')


driver.close()