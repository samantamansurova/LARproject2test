import os
import re
import time
import datetime
import tkinter as tk
from tkinter import OptionMenu, Button, ttk
from selenium.webdriver.common.by import By
from icalendar import Calendar, Event
from selenium.webdriver.chrome.options import Options
from selenium import webdriver


def open_file_explorer():
    directory = os.path.dirname(os.path.abspath(__file__))
    os.system(f'explorer "{directory}"')



def scrape(kurss, grupa, progress_var, window):
    chrome_options = Options()
    chrome_options.add_argument('--headless')

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://nodarbibas.rtu.lv/")

    darbiba1 = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[1]/div/div/div/div[2]/div/button/div/div/div')
    darbiba1.click()
    time.sleep(0.5)

    darbiba2 = driver.find_element(By.XPATH,
                                   '/html/body/div[2]/div/div[1]/div/div/div/div[2]/div/div/div[2]/ul/li[11]/a')
    darbiba2.click()
    time.sleep(0.5)

    darbiba3 = driver.find_element(By.XPATH, kurss)
    darbiba3.click()
    time.sleep(0.5)

    darbiba4 = driver.find_element(By.XPATH, grupa)
    darbiba4.click()
    time.sleep(0.5)

    darbiba5 = driver.find_element(By.XPATH,'/html/body/div[2]/div/div[2]/div/div/div[1]/div[2]/div[1]/div[3]/div/button[1]/span')
    click_count = 4
    for i in range(click_count):
        darbiba5.click()
    time.sleep(0.5)

    events = []
    events.clear()

    def get_events():
        nonlocal events

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
            print("lapa clicked")

        return events

    time.sleep(0.5)

    darbiba6 = driver.find_element(By.XPATH,'/html/body/div[2]/div/div[2]/div/div/div[1]/div[2]/div[1]/div[3]/div/button[5]/span')
    click_count = 5
    for i in range(click_count):
        events.extend(get_events())
        darbiba6.click()
        progress_var.set((i + 1) * 100 // click_count)
        window.update()

    saraksts = []

    for duplikats in events:
        if duplikats not in saraksts:
            saraksts.append(duplikats)

    for event in saraksts:
        print(event)

    for idx, item in enumerate(saraksts):
        if "Terminoloģijas minimums ( angļu valodā )" in item["title"]:
            cleaned_item = re.sub(r'\((.*?)\)', r'\1', item["title"], 1)
            item["title"] = cleaned_item

    locations = {
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

    ending = ", Latvia"
    cal = Calendar()
    cal.add('prodid', '-//Kalendars//mxm.dk//')
    cal.add('version', '1.0')

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

        date_obj = datetime.datetime.strptime(date_str, '%Y. gada %d. %B')
        time_start_obj = datetime.datetime.strptime(time_str_start, '%H:%M')
        time_end_obj = datetime.datetime.strptime(time_str_end, '%H:%M')

        short_date_format = date_obj.strftime('%d/%m/%Y')
        short_time_format_start = time_start_obj.strftime('%H:%M')
        short_time_format_end = time_end_obj.strftime('%H:%M')

        event.add('dtstart',
                  datetime.datetime.strptime(f"{short_date_format} {short_time_format_start}", "%d/%m/%Y %H:%M"))
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

    with open('kalendars.ics', 'wb') as my_file:
        my_file.write(cal.to_ical())

    print("ICS created")
    time.sleep(2)

    driver.close()

    return 'my.ics'


def update_options(*args):
    global drop1
    selected_kurss = click.get()

    if selected_kurss == "1. kurss":
        options_grupa = ["1. grupa", "2. grupa", "3. grupa", "4. grupa", "5. grupa", "6. grupa"]
    elif selected_kurss == "2. kurss":
        options_grupa = ["1. grupa", "2. grupa", "3. grupa", "4. grupa", "5. grupa"]
    elif selected_kurss == "3. kurss":
        options_grupa = ["1. grupa", "2. grupa", "3. grupa", "4. grupa"]
    else:
        options_grupa = []

    if drop1:
        drop1.destroy()

    click1.set("Izvēlies grupu")
    drop1 = OptionMenu(window, click1, *options_grupa)
    drop1.config(width=12)
    #drop1.pack(side="left")
    drop1.grid(column=1, row=0)


def setKurss():
    return click.get()


def setGrupa():
    return click1.get()


def callScrape():
    for widget in window.winfo_children():
        if isinstance(widget, tk.Label) and widget.cget("text") == "Atvērt kalendāra atrašanās vietu":
            widget.destroy()


    dropdownKurss = setKurss()
    dropdownGrupa = setGrupa()

    progress_var = tk.IntVar()
    progress_var.set(0)

    progress = ttk.Progressbar(window, variable=progress_var, length=200, mode='determinate')
    progress.grid(row=2, column=0, columnspan=5, pady=10)

    if dropdownKurss == "1. kurss":
        kurss = '/html/body/div[2]/div/div[1]/div/div/div/div[3]/div[1]/div[1]/select/option[2]'
        if dropdownGrupa == "1. grupa":
            grupa = '/html/body/div[2]/div/div[1]/div/div/div/div[3]/div[1]/div[2]/select/option[2]'
        elif dropdownGrupa == "2. grupa":
            grupa = '/html/body/div[2]/div/div[1]/div/div/div/div[3]/div[1]/div[2]/select/option[3]'
        elif dropdownGrupa == "3. grupa":
            grupa = '/html/body/div[2]/div/div[1]/div/div/div/div[3]/div[1]/div[2]/select/option[4]'
        elif dropdownGrupa == "4. grupa":
            grupa = '/html/body/div[2]/div/div[1]/div/div/div/div[3]/div[1]/div[2]/select/option[5]'
        elif dropdownGrupa == "5. grupa":
            grupa = '/html/body/div[2]/div/div[1]/div/div/div/div[3]/div[1]/div[2]/select/option[6]'
        elif dropdownGrupa == "6. grupa":
            grupa = '/html/body/div[2]/div/div[1]/div/div/div/div[3]/div[1]/div[2]/select/option[7]'
    elif dropdownKurss == "2. kurss":
        kurss = '/html/body/div[2]/div/div[1]/div/div/div/div[3]/div[1]/div[1]/select/option[3]'
        if dropdownGrupa == "1. grupa":
            grupa = '/html/body/div[2]/div/div[1]/div/div/div/div[3]/div[1]/div[2]/select/option[2]'
        elif dropdownGrupa == "2. grupa":
            grupa = '/html/body/div[2]/div/div[1]/div/div/div/div[3]/div[1]/div[2]/select/option[3]'
        elif dropdownGrupa == "3. grupa":
            grupa = '/html/body/div[2]/div/div[1]/div/div/div/div[3]/div[1]/div[2]/select/option[4]'
        elif dropdownGrupa == "4. grupa":
            grupa = '/html/body/div[2]/div/div[1]/div/div/div/div[3]/div[1]/div[2]/select/option[5]'
        elif dropdownGrupa == "5. grupa":
            grupa = '/html/body/div[2]/div/div[1]/div/div/div/div[3]/div[1]/div[2]/select/option[6]'
    elif dropdownKurss == "3. kurss":
        kurss = '/html/body/div[2]/div/div[1]/div/div/div/div[3]/div[1]/div[1]/select/option[4]'
        if dropdownGrupa == "1. grupa":
            grupa = '/html/body/div[2]/div/div[1]/div/div/div/div[3]/div[1]/div[2]/select/option[2]'
        elif dropdownGrupa == "2. grupa":
            grupa = '/html/body/div[2]/div/div[1]/div/div/div/div[3]/div[1]/div[2]/select/option[3]'
        elif dropdownGrupa == "3. grupa":
            grupa = '/html/body/div[2]/div/div[1]/div/div/div/div[3]/div[1]/div[2]/select/option[4]'
        elif dropdownGrupa == "4. grupa":
            grupa = '/html/body/div[2]/div/div[1]/div/div/div/div[3]/div[1]/div[2]/select/option[5]'

    ics_filename = scrape(kurss, grupa, progress_var, window)

    progress_var.set(100)
    window.update()

    if ics_filename:
        for widget in window.winfo_children():
            if isinstance(widget, tk.Label) and widget.cget("text") == "Atvērt kalendāra atrašanās vietu":
                widget.destroy()

        link_label = tk.Label(window, text="Atvērt kalendāra atrašanās vietu", cursor="hand2", fg="blue")
        link_label.grid(row=3, column=0, columnspan=5, pady=5)
        link_label.bind("<Button-1>", lambda e: open_file_explorer())


window = tk.Tk()
window.title("RTU IT studiju programmas kalendārs")
window.iconphoto(False, tk.PhotoImage(file='download.png'))

window.minsize(352,32) #tkinter loga fiksetais izmers
window.maxsize(352,136)

options_kurss = ["1. kurss", "2. kurss", "3. kurss"]
click = tk.StringVar()
click.set("Izvēlies kursu")
drop = OptionMenu(window, click, *options_kurss)
#drop.pack(side="left")
drop.grid(column=0, row=0)
click.trace('w', update_options)

options_grupa = ["1. grupa", "2. grupa", "3. grupa", "4. grupa", "5. grupa", "6. grupa"]
click1 = tk.StringVar()
click1.set("Izvēlies grupu")
drop1 = OptionMenu(window, click1, *options_grupa)
#drop1.pack(side="left")
drop1.grid(column=1, row=0)

kalendarsButton = Button(window, text="Kalendārs", width=15, command=callScrape)
#kalendarsButton.pack(side="right")
kalendarsButton.grid(column=3, row=0)


window.mainloop()
