from selenium import webdriver
import pyautogui
import time
from selenium.webdriver.common.keys import Keys
import random
import string
#import sys
#path ='/home/ashwin/Downloads/geckodriver'
#sys.path.append(path)

browser = webdriver.Firefox()
elem = browser.get('http://127.0.0.1:8000/user_login')
time.sleep(5)

def brute():
	username = browser.find_element_by_id("id_username").click()
	time.sleep(2)
	pyautogui.typewrite("ashwin",interval=0.01)
	time.sleep(2)
	password = browser.find_element_by_id("id_password").click()
	time.sleep(2)
	res = ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k = 5))
	pyautogui.typewrite(res,interval=0.01)
	time.sleep(2)
	button = browser.find_element_by_class_name("registerbtn").click()
	time.sleep(3)

for i in range(5):
	brute()




