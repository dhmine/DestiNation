# -*- coding: utf-8 -*-
"""
Created on 20-09-2022
@author: DHMINE Mohamed
"""

#import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup as bs
import pandas as pd
from pandas import DataFrame
from selenium.webdriver.common.action_chains import ActionChains
# default path to file to store data
from selenium.webdriver.common.by import By
import csv
import time

hotel = []
url = []

url = "https://www.tripadvisor.com/Hotels-g187070-France-Hotels.html"
domain = 'https://www.tripadvisor.com'
#req = requests.get(url)

""""" contenu = req.content
soup = bs(contenu, "html.parser")

tousLesLiens = soup.findAll('a')

print(len(tousLesLiens)) """""

driver = webdriver.Firefox(executable_path = "C:/Users/Mohamed/Documents/SmartROI/geckodriver.exe")
driver.maximize_window()
driver.get(url)
time.sleep(1)
# acceptation des cookies
element = driver.find_element(by="xpath", value="//button[@id='onetrust-accept-btn-handler']")
ActionChains(driver).move_to_element(element).click().perform()

#driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


i = 0
linkss = []
while i < 115:
    try :
        more = driver.find_element(by="xpath", value="//span[@class='nav next ui_button primary']")
        driver.execute_script("arguments[0].click();", more)
        link_list = driver.find_elements(by="xpath", value="//a[@class = 'property_title prominent']")
        links = list(map(lambda hotel_link: hotel_link.get_attribute("href"),
                     driver.find_elements(by="xpath", value="//a[contains(@class, 'property_title prominent')]")))
        linkss.append(links)
        time.sleep(5)

    except :
        link_list = 'none'
    i += 1

link_flat = []
for sublist in linkss:
    for item in sublist:
        link_flat.append(item)

d1 = {"url": link_flat}
df = pd.DataFrame.from_dict(d1)
df.to_excel('France_Hotel_links.xlsx')

print(link_flat)
