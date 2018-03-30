import time
import re
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
import selenium
from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.proxy import *
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

## Helper functions

"""
#1 open_url_prod
- Open supplied url in the browser window
"""

def sleep_script(seconds='normal'):
	if seconds == 'normal':
		time.sleep(4)
		return
	else:
		time.sleep(seconds)
		return

def init_browser(type='firefox', options={'headless': False, 'maximize_window': True}):
	## Initialize Firefox browser
	options = Options()
	options.add_argument("--headless")
	# browser = webdriver.Firefox(firefox_options=options)
	browser = webdriver.Firefox()
	## Maximize window and open the base url
	browser.maximize_window()
	return browser

def my_proxy(PROXY_HOST,PROXY_PORT):
        fp = webdriver.FirefoxProfile()
        # Direct = 0, Manual = 1, PAC = 2, AUTODETECT = 4, SYSTEM = 5
        print PROXY_PORT
        print PROXY_HOST
        fp.set_preference("network.proxy.type", 1)
        fp.set_preference("network.proxy.http",PROXY_HOST)
        fp.set_preference("network.proxy.http_port",int(PROXY_PORT))
        fp.set_preference("general.useragent.override","whater_useragent")
        fp.update_preferences()
        return webdriver.Firefox(firefox_profile=fp)

def open_url(browser, url):
	print("Loading "+ str(url))
	repeat = False
	while not repeat:
		try:
			browser.get(url)
			sleep_script()
			repeat = True
		except:
			print("Something went wrong loading the requested page, trying again!")
			repeat = False
	print("Page loaded successfully")
	return True

def open_url_dev(browser, url):
	browser.get(url)
	sleep_script()
	return True

def write_to_file(data, filename):
	print("Generating CSV data")
	pin = open(filename,"a+")
	pin.write(data+"\n")
	pin.close()
	print("End of program")

def write_chunk_to_file(data_set, filename):
	with open(filename, 'a+') as f:
		writer = csv.writer(f)
		writer.writerows(data_set)
	print("Write successful!")
	return True

def read_as_soup(browser):
	allHTML = BeautifulSoup(browser.page_source)
	html=allHTML.encode('utf-8')
	return BeautifulSoup(html, 'html.parser')


"""
Converting image from thumb to full width
https://cdn-img-feed.streeteasy.com/nyc/image/38/311361438.jpg
full width image will be
https://cdn-img-feed.streeteasy.com/nyc/image/37/311361437.jpg
"""
def get_full_img_path(url):
	img_url_set = url.split("/")
	thumb_index = img_url_set[len(img_url_set)-2]
	full_index = int(thumb_index)-1
	img_url_set[len(img_url_set)-2] = str(full_index)

	image_name = img_url_set[len(img_url_set)-1].split(".")[0]
	image_ext = img_url_set[len(img_url_set)-1].split(".")[1]

	image_name_without_index = re.sub(thumb_index+"$", '', image_name)#image_name.split(thumb_index, 1)[0]
	# image_name_index = image_name.split(thumb_index, 1)[1]
	img_url_set[len(img_url_set)-1] = image_name_without_index+str(full_index)+"."+image_ext
	return "".join(img_url_set)

"""
"""
def login_user(browser, url, username, password):
	print("Opening login page")
	open_url(browser, url)
	
	## Click to open the login modal
	browser.find_element(By.CLASS_NAME, 'headerSignIn').click()

	sleep_script(5)
	html = browser.execute_script("document.getElementsByTagName('html')[0].innerHTML")
	
	## Fill login form
	browser.execute_script("document.getElementById(\'loginEmail\').value=\'"+username+"\';")
	sleep_script(2)
	browser.execute_script("document.getElementById(\'loginPassword\').value=\'"+password+"\';")
	# browser.find_element(By.XPATH, "//input[@id='loginEmail']").click().send_keys(username)
	# browser.find_element(By.XPATH, "//input[@id='loginPassword']").click().send_keys(password)
	sleep_script(2)
	## Submit login form and try logging in
	browser.execute_script("document.getElementById(\'signIn\').click()")
	print("Login attempted")
	sleep_script(12)
	return True


"""
	Selecting an option from the supplied select options parent
	jQuery(".bootstrap-select.beds").find('li a span:contains(1.0)').parent().trigger("click")
"""
def form_select_option(browser, jQuerySelector, val_to_select):
	script = "jQuery(\"%s\").val(\'%s\');" % (jQuerySelector, val_to_select)
	script += "jQuery(\""+ jQuerySelector +"\").trigger(\'change\');"
	sleep_script()
	browser.execute_script(script)
	sleep_script()
	return True

def execute_script(browser, script):
	browser.execute_script(script)
	sleep_script()
	return True

"""
	Inserting text in the input[type=text] field
	jQuery("#sf-clone").val("12")
"""
def form_input_text(browser, selector, val, js=False, index=False):
	if not js:
		browser.find_element_by_id(selector).send_keys(Keys.CONTROL+"a")
		browser.find_element_by_id(selector).send_keys(Keys.BACKSPACE)
		browser.find_element_by_id(selector).send_keys(val)
	else:
		if not index:
			script = "jQuery(document).find(\""+ selector +"\").val(\'"+ val +"\');"
			script += "jQuery(document).find(\""+ selector +"\").trigger(\'change\');"
		else:
			script = "jQuery('"+ selector +"').eq(\'"+str(index)+"\').val('"+ val +"');"
			script += "jQuery('"+ selector +"').eq(\'"+str(index)+"\').trigger(\'change\');"
		sleep_script()
		# print("Executing script"+ script)
		browser.execute_script(script)
	
	sleep_script()
	return True

"""
	Select from radio elements
	jQuery("#listingTypeRadios").find('input[type="radio"]')[1].click()
	jQuery("#listingTypeRadios").find('label span:contains("Single")').click()
"""
def form_select_radio(browser, selector, val):
	script = "jQuery(\"%s\").find(\"label span:contains(\'%s\')\").eq(0).parent().prev().click();" % (selector, val)
	# script = "return jQuery('%s').find('label span:contains(%s)').eq(0).click();" % (selector, val)
	# script = "jQuery('#listingTypeRadios').find('label span:contains(\"Single\")').click()"
	sleep_script()
	# try:
	browser.execute_script(script)
	# except:
	# do nothing
	# print("Exception was encountered, continuing")
	sleep_script()
	return True

"""
	Select checkbox
	jQuery("#hideContact").prop('checked', true)
"""
def form_select_checkbox(browser, selector, js=False):
	if not js:
		sleep_script()
		# script = "jQuery(\"%s\").prop('checked', true)" % (selector)
		# browser.execute_script(script)
		browser.find_element_by_id(selector).click()
		sleep_script()
		return True
	if not index:
		script = "jQuery(document).find(\""+ selector +"\").prop('checked', true);"
		script += "jQuery(document).find(\""+ selector +"\").trigger(\'change\');"
	else:
		script = "jQuery('"+ selector +"').eq(\'"+str(index)+"\').prop('checked', true);"
		script += "jQuery('"+ selector +"').eq(\'"+str(index)+"\').trigger(\'change\');"
	sleep_script()
	# print("Executing script"+ script)
	browser.execute_script(script)
	return True

"""
	Button click
"""
def form_button_click(browser, selector):
	sleep_script()
	script = "jQuery(\'"+selector+"\').click()"
	browser.execute_script(script)
	sleep_script()
	return True

"""
	For uploading file
"""
def form_upload_file(browser, xpath_selector, file):
	script = "jQuery(\"div.photosWrapper div.grid input[type=\'file\']\").css(\'display\', \'block\')"
	browser.execute_script(script)
	sleep_script()
	browser.find_element(By.XPATH, xpath_selector).send_keys(file)
	sleep_script(30)
	print("File sent for upload")
	return True


"""
	General utility
	Print action being performed
"""
def display_notice(type, message):
	print(message)
	return True