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

m = p.findChildren("option");


'''
f = {}
for n in m[1:]:
	driver.find_element_by_css_selector("select#courseprefix > option[value='" + n.text + "']").click()
	driver.find_element_by_xpath(".//input[@type='submit' and @title='Search Database']").click()
	els = driver.find_elements_by_css_selector("td.width")
	p = []
	#print(n.text)
	for el in els:
		matchObj = re.search(r'\d{4}', el.text,  re.M|re.I)
		if matchObj:
			#print(matchObj.group())
			p.append(matchObj.group())
		else:
			print("fuck")
	f[n.text] = p

with open('programList.json', 'w') as outfile:
    json.dump(f, outfile)

print(json.dumps(f))
'''

# REPLACE ALL DRIVER ELEMENT PARSING WITH BEAUTIFUL SOUP !!!!

f = {}
for n in m[1:2]:
	driver.find_element_by_css_selector("select#courseprefix > option[value='" + n.text + "']").click()
	driver.find_element_by_xpath(".//input[@type='submit' and @title='Search Database']").click()
	els = driver.find_elements_by_css_selector("td.width > a")
	c = []
	print(n.text)
	print("-----------------------")
	for el in els:
		print(el.text)
		p = {}
		#print(c)
		# Open
		el.click()
		time.sleep(2)

		# works here
		#e = driver.find_element_by_css_selector("a.link-open.td_dark.preview_td")
		#e.click()
		#time.sleep(2)	

		clas = driver.find_element_by_class_name("ajaxcourseindentfix")		
		title = clas.find_element_by_css_selector("h3")
		#print("CUCK - " + title.text)
		p["name"] = title.text 
		p["course_title"] = "test" # seperate name from course prefix...

		credits = clas.find_elements_by_css_selector("strong")
		p["credits"] = credits[1].text # get 2nd strong element
		# Get credit type to fulfill degree requirments
		p["credit_type"] = "test"

		# How can I pull data from what professors are teaching this class and when?
		p["professors"] = "test"

		# Lab and Field work Hours
		#c["lab_field"] = "test"

		# Contact Hours
		#p["contact"] = "test"

		# Offered jointly with?
		p["offered_with"] = "test"

		# Course description - this will be difficult to pull out
		p["description"] = "test"

		c.append(p)
		#print(c)

		choice_preqList = []
		required_preqList = []
		new = BeautifulSoup(driver.page_source, "html.parser")
		n = new.find(class_="ajaxcourseindentfix")

		#e = driver.find_element_by_css_selector("a.link-open.td_dark.preview_td")
		#e.click()
		#time.sleep(2)	 fucking works here??

		prereqs = n.get_text()
		preq = re.search(r'Prerequisite.*?Corequisite', prereqs, re.M|re.I)
		preq1 = preq.group(0)
		pre = re.findall(r'\w{3} \d{4}.?', preq1, re.M|re.I)
		if pre:
			print("PREREQS: ")
			print(pre)
			#print(pre.groups())
			for g in pre:
				#print(g)
				required_preqList.append({"name" : g})
			print("END OF PREREQS")

		e = driver.find_element_by_css_selector("a.link-open.td_dark.preview_td")
		e.click()
		time.sleep(2)	

        p["choice_prereqs"] = choice_preqList # can probably remove this or use it for soft prereqs
        p["required_prereqs"] = required_preqList

        # Close - this isnt working?
        #e = driver.find_element_by_css_selector("a.link-open.td_dark.preview_td")
        #e.click()
        #time.sleep(2)	

        # c.append(p)
        print(c)
	print("-----------------------")
f = c
#print(f)
#print(len(f))

def recurse(m, is_preqFor):
    for h in reversed(f):
        if any(g["name"] == m["name"] for g in h["required_prereqs"]):
            h["type"] = "required"
            is_preqFor.append(h)
            f.remove(h)
            recurse(h, [])
        # Append choice prereqs to children, give them choice attribute for color encoding
        elif any(g["name"] == m["name"] for g in h["choice_prereqs"]):
            h["type"] = "choice"
            is_preqFor.append(h)
    # append children to course if they exist
    m["children"] = is_preqFor

# beginning of recursive call
for d in f:
    recurse(d, [])
    

print(f)

try:
    outfile = open('outputUCF.json', 'w')
    json.dump(f, outfile)
    outfile.close()
except ValueError:
    print "FUCK"
        

''' Trying to expand popup
driver.find_element_by_css_selector("#gateway-toolbar-1 > div.gateway-toolbar-print.gateway-toolbar-item").click()
time.sleep(2)
driver.switch_to_alert();
driver.find_element_by_css_selector("body > table > tbody > tr:nth-child(3) > td.block_n2_and_content > table > tbody > tr:nth-child(2) > td.block_content_outer > table > tbody > tr > td > div:nth-child(7) > a:nth-child(1)").click()
'''

driver.close()

