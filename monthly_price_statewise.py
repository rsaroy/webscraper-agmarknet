"""
! Use Python 2.7 !

Gets state wise monthly wholesale price of crops in crops.txt in working direc
from agmarknet.gov.in
"""
import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import Select
# Geckodriver was slow to load homepage, hence used 'eager' capability
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import csv
from bs4 import BeautifulSoup

# Function 1 - see if years are selectable in the year box


def try_year():
    year_box = browser.find_element_by_id('cphBody_Year_list')
    indicator_year_options_loaded = False
# this while loop chunk forces the program to keep trying till field loads
    while not indicator_year_options_loaded:
        try:
            year_box = browser.find_element_by_id('cphBody_Year_list')
            years_list = year_box.find_elements_by_tag_name('option')
            if len(years_list) > 1:
                print 'year options loaded'
                indicator_year_options_loaded = True
                return years_list
            else:
                year_box = browser.find_element_by_id('cphBody_Year_list')
                time.sleep(1)
                print 'loading year options'

        except selenium.common.exceptions.StaleElementReferenceException:
            print 'stale year_options'
            time.sleep(1)
        except selenium.common.exceptions.NoSuchElementException:
            print 'nosuch year_options'
            time.sleep(1)

# Function 2- Select/Input the year
# There is duplicity of code since selenium elements often go stale and need
# to be reloaded


def year_options(year):
    indicator23 = False
    while not indicator23:
        try:
            year_box = browser.find_element_by_id('cphBody_Year_list')
            select = Select(year_box)
            select.select_by_visible_text(year)
            indicator23 = True
        except selenium.common.exceptions.StaleElementReferenceException:
            print 'stale selectyear'
            time.sleep(1)
        except selenium.common.exceptions.NoSuchElementException:
            print 'nosuch selectyear'
            time.sleep(1)

# Function 3 - see if months are selectable in month box


def try_month():
    print "try_month"
    indicator_month_options_loaded = False
    while not indicator_month_options_loaded:
        try:
            month_box = browser.find_element_by_id('cphBody_Month_list')
            months_list = month_box.find_elements_by_tag_name('option')
            if len(months_list) > 1:
                print 'month options loaded'
                indicator_month_options_loaded = True
                return months_list
            else:
                month_box = browser.find_element_by_id('cphBody_Month_list')
                time.sleep(1)
                print 'month options loading'

        except selenium.common.exceptions.StaleElementReferenceException:
            print 'stale month_options'
            time.sleep(1)
        except selenium.common.exceptions.NoSuchElementException:
            print 'nosuch month_options'
            time.sleep(1)

# Function 4 - select the month


def month_options(month):
    indicator24 = False
    while not indicator24:
        try:
            month_box = browser.find_element_by_id('cphBody_Month_list')
            select = Select(month_box)
            months_list = month_box.find_elements_by_tag_name('option')
            select.select_by_visible_text(month)
            indicator24 = True
        except selenium.common.exceptions.StaleElementReferenceException:
            print 'stale selectmonth'
            time.sleep(1)
        except selenium.common.exceptions.NoSuchElementException:
            print 'nosuch selectmonth'
            time.sleep(1)

# Function 5 - Submit button


def select_1():
    indicator3 = False
    while not indicator3:
        try:
            print 'select_submit 1'
            submit_box = browser.find_element_by_name('ctl00$cphBody$But_Submit')
            indicator3 = True
        except selenium.common.exceptions.NoSuchElementException:
            print 'select_submit exception'
            time.sleep(1)
    submit_box.click()

# Function 6 - Check if output table ready


def table_loaded():
    indicator2 = False
    while not indicator2:
        try:
            browser.find_element_by_link_text('Main Menu')
            indicator2 = True
        except selenium.common.exceptions.NoSuchElementException:
            time.sleep(1)

# Function 7 - Get the data (state, price) into a vector


def table_extractor(src, crop, year, month):
    entry3 = []
    soup = BeautifulSoup(src)
    table = soup.find('table', id="cphBody_DataGrid_PriMon")
    rows = table.tbody.find_all('tr')
    for row in rows[1:]:
        entry2 = []
        state_cell = row.contents[1]
        state = state_cell.text
        price_cell = row.contents[2]
        price = price_cell.text
        entry2.append(crop.encode('utf-8'))
        entry2.append(year.encode('utf-8'))
        entry2.append(month.encode('utf-8'))
        entry2.append(state.encode('utf-8'))
        entry2.append(price.encode('utf-8'))
        entry3.append(entry2)
    return entry3

# Function 8- select year after going back to form


def fill_year(year):
    indicatorx1 = False
    while not indicatorx1:
        try:
            try_year()
            indicatorx1 = True

        except selenium.common.exceptions.NoSuchElementException:
            time.sleep(1)
    indicatorx2 = False
    while not indicatorx2:
        try:
            year_options(year)
            indicatorx2 = True
        except selenium.common.exceptions.NoSuchElementException:
            time.sleep(1)
    print year

# Function 9 - select year after going back to form


def fill_crop(crop):
    indicator25 = False
    while not indicator25:
        try:
            commodity_box = browser.find_element_by_xpath("//select[@id='cphBody_Commodity_list']")
            select = Select(commodity_box)
            select.select_by_visible_text(crop)
            indicator25 = True
        except selenium.common.exceptions.StaleElementReferenceException:
            print 'stale selectcrop'
            time.sleep(1)
        except selenium.common.exceptions.NoSuchElementException:
            print 'nosuch selectcrop'
            time.sleep(1)


# Opening a wordfile in working directory containing list of crops
wordfile = open(r'crops.txt', "r")
csv_object = csv.reader(wordfile)
wordlist_kacchi = list(csv_object)
wordlist = []
for entry in wordlist_kacchi:
    entry_ = str(entry)
    word1 = entry_.lstrip("['")
    word2 = word1.rstrip("']")
    wordlist.append(word2)
# Now we have processed it into an iterable list of crops - wordlist_kacchi

# initialising geckodriver
caps = DesiredCapabilities().FIREFOX
caps["pageLoadStrategy"] = "eager"
pathtogecko = '/Users/rajas/Desktop/Python Projects/Firefox_GeckoDriver/geckodriver'
browser = webdriver.Firefox(executable_path=pathtogecko)
url = 'http://www.agmarknet.gov.in/PriceTrends/SA_Pri_Month.aspx'
browser.get(url)

for crop in wordlist:

    #filling in crop
    commodity_box = browser.find_element_by_xpath("//select[@id='cphBody_Commodity_list']")
    select = Select(commodity_box)
    select.select_by_visible_text(crop)

# getting available years for this crop
    yearlist_webelements = try_year()
    yearlist = []
    for year_webelement in yearlist_webelements:
        year_text = year_webelement.text
        yearlist.append(year_text)

# Loop1 - iterating over year
    for year in yearlist[1:]:
        indicator = False
        print year

# checking if year box ready to fill
        while not indicator:
            try:
                year_options(year)
                indicator = True
            except selenium.common.exceptions.NoSuchElementException:
                time.sleep(1)
        indicator = False

# checking if month box ready to fill
        while not indicator:
            try:
                monthlist_webelement = try_month()
                indicator = True
            except selenium.common.exceptions.NoSuchElementException:
                time.sleep(1)
            except selenium.common.exceptions.StaleElementReferenceException:
                time.sleep(1)

# fetching available months for this (crop, year)
        monthlist = []
        for month_element in monthlist_webelement:
            month_text = month_element.text
            monthlist.append(month_text)

# Loop 2- iterating over months
        for month in monthlist[1:]:
            print month
            indicator = False
            while not indicator:
                try:
                    month_box = browser.find_element_by_id('cphBody_Month_list')
                    select_month = Select(month_box)
                    select_month.select_by_visible_text(month)
                    indicator = True
                except selenium.common.exceptions.NoSuchElementException:
                    time.sleep(1)
                except selenium.common.exceptions.StaleElementReferenceException:
                    time.sleep(1)
# clicking submit box
            select_1()
# checking if table is ready after submitting form
            table_loaded()
            src = browser.page_source
# getting table with table_extractor function
            entryy = table_extractor(src, crop, year, month)
# writing to file
            with open("output.csv", "a") as f:
                writer = csv.writer(f)
                writer.writerows(entryy)
            back_button = browser.find_element_by_link_text('Back')
            back_button.click()
# filling in crop and year for next month's iteration
            fill_crop(crop)
            fill_year(year)
