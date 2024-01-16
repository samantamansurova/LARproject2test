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

#locale.setlocale(locale.LC_TIME, "latvian")
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
time.sleep(2)

events = []
events.clear()

iter = 0

def get_events():
    global iter


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
        iter += 1
        print(iter)

        ##driver.quit()

    return events

time.sleep(1)

darbiba6= driver.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/div/div/div[1]/div[2]/div[1]/div[3]/div/button[5]/span')
click_count= 5
for i in range(click_count):
    events.extend(get_events())
    darbiba6.click()
    time.sleep(1)


saraksts = []

#Duplikātu pārbaude
for duplikats in events:
    if duplikats not in saraksts:
        saraksts.append(duplikats)

for event in saraksts:
    print(event)



for idx, item in enumerate(saraksts):
    if "Terminoloģijas minimums ( angļu valodā )" in item["title"]:
        cleaned_item = re.sub(r'\((.*?)\)', r'\1', item["title"], 1)
        item["title"] = cleaned_item


locations ={
"Att": " Attālināti",
"Nen": " Nenoteikta",
"Pie": " Piebalgas iela, Cēsis",
"Smi": " Smilšu iela, Daugavpils",
"Bra": " Braslas iela, Jūrmala",
"Upm": " Upmalas iela, Jūrmala",
"Aiv": " Aiviekstes iela, Rīga",
"Aus": " Ausekļa iela, Rīga",
"Āze": " Āzenes iela, Rīga",
"Bal": " Balasta Dambis, Rīga",
"Bie": " Biešu iela, Rīga",
"Bur": " Burtnieku iela, Rīga",
"Dau": " Daugavgrīvas iela, Rīga",
"Enk": " Enkura iela, Rīga",
"Ind": " Indriķa iela, Rīga",
"Kal": " Kalnciema iela, Rīga",
"Kro": " Kronvalda bulvāris, Rīga",
"Ķīp": " Ķīpsalas iela, Rīga",
"Lai": " Laimdotas iela, Rīga",
"Lau": " Lauvas iela, Rīga",
"Lom": " Lomonosova iela, Rīga",
"Mež": " Meža iela, Rīga",
"Ola": " Olaines iela, Rīga",
"Pul": " Pulka iela, Rīga",
"Sēt": " Sētas iela, Rīga",
"Val": " Paula iela, Valdena",
"Vis": " Viskaļu iela, Rīga",
"Zun": " Zunda krastmala, Rīga",
"Kul": " Kuldīgas iela, Ventspils"
}




ending =  ", Latvia"
cal = Calendar()
cal.add('prodid', '-//Kalendars//mxm.dk//')
cal.add('version', '1.0')
##locale.setlocale(locale.LC_TIME, "latvian")




month_mapping = {
    'janvāris': 'January',
    'februāris': 'February',
    'marts': 'March',
    'aprīlis': 'April',
    'maijs': 'May',
    'jūnijs': 'June',
    'jūlijs': 'July',
    'augusts': 'August',
    'septembris': 'September',
    'oktobris': 'October',
    'novembris': 'November',
    'decembris': 'December'
}


def replace_month_names(text):
    for latvian_month, english_month in month_mapping.items():
        text = text.replace(latvian_month, english_month)
    return text

for a in saraksts:
    event = Event()
    event.add('summary', replace_month_names(a["title"]))

    date_str = replace_month_names(a['date'])
    time_str_start, time_str_end = a['time'].split(' - ')

    # Parse the date and time
    date_obj = datetime.datetime.strptime(date_str, '%Y. gada %d. %B')
    time_start_obj = datetime.datetime.strptime(time_str_start, '%H:%M')
    time_end_obj = datetime.datetime.strptime(time_str_end, '%H:%M')

    # Format the date and time in "dd/mm/yyyy" format
    short_date_format = date_obj.strftime('%d/%m/%Y')
    short_time_format_start = time_start_obj.strftime('%H:%M')
    short_time_format_end = time_end_obj.strftime('%H:%M')

    event.add('dtstart', datetime.datetime.strptime(f"{short_date_format} {short_time_format_start}", "%d/%m/%Y %H:%M"))
    event.add('dtend', datetime.datetime.strptime(f"{short_date_format} {short_time_format_end}", "%d/%m/%Y %H:%M"))
    event.add('dtstamp', datetime.datetime.now())

    title_parts = a["title"].split("(")
    if len(title_parts) > 1:
        addr_parts = title_parts[1].split(")")
        if len(addr_parts) > 0:
            addr = addr_parts[0].split("-")[0].split(".")
            event.add('location', locations.get(addr[0], "") + " " + addr[1] + ending)

    defised = a["title"].split("-")
    event.add('description', defised[len(defised) - 1].split(")")[0])

    cal.add_component(event)


with open('my.ics', 'wb') as my_file:
    my_file.write(cal.to_ical())

time.sleep(2)

driver.close()
