from bs4 import BeautifulSoup
import re, json, pickle, glob, csv, time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium import webdriver

url = 'http://catalog.ucf.edu/content.php?catoid=3&navoid=174&returnto=portfolio&in_portfolio=1'

driver = webdriver.Chrome()
driver.get(url)

element = driver.find_element_by_id("courseprefix")

courseList = BeautifulSoup(driver.page_source, "html.parser")

p = courseList.find(id="courseprefix")

m = p.findChildren("option")

f = {}

for n in m[1:]:
    driver.find_element_by_css_selector("select#courseprefix > option[value='" + n.text + "']").click()
    driver.find_element_by_xpath(".//input[@type='submit' and @title='Search Database']").click()
    els = driver.find_elements_by_css_selector("td.width")
    p = []
    print(n.text)
    for el in els:
        matchObj = re.search(r'\d{4}?[a-z]', el.text, re.M|re.I)
        if matchObj:
            print(matchObj.group())
            p.append(matchObj.group())
        else:
            matchObj = re.search(r'\d{4}', el.text, re.M|re.I)
            if matchObj:
                print(matchObj.group())
                p.append(matchObj.group())
            else:
                print("error")
                f[n.text] = p
        f[n.text] = p

with open('programList.json', 'w') as outfile:
    json.dump(f, outfile)


driver.close()
