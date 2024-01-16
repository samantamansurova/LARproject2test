import os

import selenium as selenium
import selenium.webdriver
import re
from selenium.webdriver.chrome.service import Service
import selenium.common
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from icalendar import Calendar, Event

import datetime
import locale

driver = webdriver.Chrome()
driver.get("https://nodarbibas.rtu.lv/")
##time.sleep(600)

##/html/body/div[2]/div/div[1]/div/div/div/div[2]/div/button/div/div/div

darbiba1= driver.find_element(By.XPATH, '/html/body/div[2]/div/div[1]/div/div/div/div[2]/div/button/div/div/div')
darbiba1.click()
time.sleep(1)

##/html/body/div[2]/div/div[1]/div/div/div/div[2]/div/div/div[2]/ul/li[11]/a

darbiba2= driver.find_element(By.XPATH, '/html/body/div[2]/div/div[1]/div/div/div/div[2]/div/div/div[2]/ul/li[11]/a')
darbiba2.click()
time.sleep(1)

##/html/body/div[2]/div/div[1]/div/div/div/div[3]/div[1]/div[1]/select/option[2]

darbiba3= driver.find_element(By.XPATH, '/html/body/div[2]/div/div[1]/div/div/div/div[3]/div[1]/div[1]/select/option[2]')
darbiba3.click()
time.sleep(1)

##/html/body/div[2]/div/div[1]/div/div/div/div[3]/div[1]/div[2]/select/option[3]

darbiba4= driver.find_element(By.XPATH, '/html/body/div[2]/div/div[1]/div/div/div/div[3]/div[1]/div[2]/select/option[3]')
darbiba4.click()
time.sleep(1)

##/html/body/div[2]/div/div[2]/div/div/div[1]/div[2]/div[1]/div[3]/div/button[1]/span

darbiba5= driver.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/div/div/div[1]/div[2]/div[1]/div[3]/div/button[1]/span')
click_count= 4
for i in range(click_count):
    darbiba5.click()
time.sleep(3)


def get_events():
    events = []

    try:

        day_events_elements = driver.find_elements(By.CLASS_NAME, 'fc-daygrid-day-events')

        for day_element in day_events_elements:

            event_harness_elements = day_element.find_elements(By.CLASS_NAME, 'fc-daygrid-event-harness')

            if event_harness_elements:
                for event_harness_element in event_harness_elements:
                    date = day_element.find_element(By.XPATH, '../..//a').get_attribute('aria-label')
                    title = event_harness_element.find_element(By.CLASS_NAME, 'fc-event-title').text
                    time = event_harness_element.find_element(By.CLASS_NAME, 'fc-event-time').text

                    events.append({
                        'date': date,
                        'title': title,
                        'time': time
                    })

    finally:

        driver.quit()

    return events


events = get_events()

for event in events:
    print(event)