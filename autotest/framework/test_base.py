from selenium import webdriver
from framework.base_page import BasePage
dr = webdriver.Firefox()
dr.get('https:www.baidu.com')
s = dr.window_handles
driver = BasePage(dr)
kw = ['id', 'kw']
driver.type(kw, 'selenium+python')
driver.my_sleep(3)
driver.type(kw, 'selenium')
su = ['id', 'su']
driver.click(su)
driver.get_img()
driver.my_sleep(2)
driver.get_title()
