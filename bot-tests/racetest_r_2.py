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
elem = browser.get('http://127.0.0.1:8000/user_register')
time.sleep(5)

def brute():
	username = browser.find_element_by_id("id_username").click()

	time.sleep(1)

	pyautogui.typewrite("akash",interval=0.01)

	time.sleep(1)

	email = browser.find_element_by_id("id_email").click()
	pyautogui.typewrite("akash1305@gmail.com",interval=0.01)

	time.sleep(1)

	p1 = browser.find_element_by_id("id_password1").click()
	pyautogui.typewrite("csgo12345",interval=0.01)

	time.sleep(1)

	p2 = browser.find_element_by_id("id_password2").click()
	pyautogui.typewrite("csgo12345",interval=0.01)

	time.sleep(2)
	button = browser.find_element_by_class_name("registerbtn").click()

input("Press Enter to continue...")

time.sleep(10)
brute()

