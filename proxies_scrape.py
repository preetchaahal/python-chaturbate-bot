# from scraping_helpers import *
import time
import re
import csv
import logging
from bs4 import BeautifulSoup
from selenium import webdriver
import selenium
from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.proxy import *
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

"""
--- TIER #1 Countries ---
Australia
Austria
Belgium
Canada
Colombia
Croatia
Czech Republic
Denmark
Finland
France
Georgia
Germany
Ireland
Israel
Italy
Korea, south
Lithuania
Luxembourg
Macedonia
Mauritius
Netherlands
New Zealand
Nicaragua
Norway
Poland
Slovak Republic
Slovenia
Spain
Sweden
Taiwan
United Kingdom
United States of America US
"""

class Proxy:
	url_for_proxy = "http://spys.one/free-proxy-list/"
	proxy_ip = None
	proxy_port = None
	browser = None
	proxies = []
	tier_1_countries_all = ['AU', 'AT', 'BE', 'CA', 'CO', 'HR', 
		 	 'CZ', 'DK', 'FI', 'GE', 'DE', 'IE', 
		 	 'IL', 'IT', 'KR', 'LT', 'LU', 'MK', 
		 	 'MU', 'NL', 'NZ', 'NI', 'NO', 'PL',
		 	 'SK', 'SI', 'ES', 'TW', 'GB', 'US']
	tier_1_countries = ['US']

	def get_browser(self):
		return self.browser

	def close_browser(self):
		self.browser.close()
		self.browser = None
		return True

	def log(self, type, data):
		logging.basicConfig(filename=self.log_file,level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
		if type == 'error':
			logging.error(data)
		else:
			logging.info(data)


	def init_browser(self, type='firefox', options={'headless': False, 'maximize_window': True}, proxy_obj=False):
		## Initialize Firefox browser
		no_options = True
		if options['headless']:
			options = Options()
			options.add_argument('-headless')
			no_options = False
		if proxy_obj == False:
			browser = webdriver.Firefox()
			self.browser = browser
		else:
			profile = self.set_proxy_profile(proxy_obj['ip'], proxy_obj['port'])
			# print(profile)
			if no_options:
				browser = webdriver.Firefox(firefox_profile = profile)
			else:
				browser = webdriver.Firefox(firefox_profile = profile, options=options)
			self.browser = browser
		browser.maximize_window()
		return browser

	def __init__(self, proxy=False):
		self.log_file = "usage.log"
		if not proxy:
			self.browser = self.init_browser('firefox', {'headless': False, 'maximize_window': True})
		else:
			print("Setting up Proxy")
			self.browser = self.init_browser('firefox', {'headless': False, 'maximize_window': True}, proxy)

	def set_proxy_profile(self, ip, port):
		profile = webdriver.FirefoxProfile()
		profile.set_preference("network.proxy.type", 1)
		profile.set_preference("network.proxy.http", ip)
		profile.set_preference("network.proxy.http_port", int(port))
		profile.set_preference("network.proxy.ssl", ip)
		profile.set_preference("network.proxy.ssl_port", int(port))
		return profile

	def is_page_blocked_by_captcha(self):
		try:
			self.browser.find_element_by_id("cf-error-details").find_element_by_xpath('/div/h1[@data-translate=\"challenge_headline\"]')
			return True
		except Exception as e:
			# print(e)
			return False

	def is_jQuery_rendered_completely(self):
		try:
			self.execute_script(self.browser, "$ === jQuery")
		except:
			return False
		return True

	def browse_url(self, url):
		browser = self.browser
		print("Loading "+ str(url))
		repeat = False
		while not repeat:
			try:
				browser.get(url)
			except:
				return False
			self.sleep_script()
			repeat = True
		print("Page loaded successfully")
		return True

	def process_proxies(self):

		for country in self.tier_1_countries:
			self.open_url(self.browser, self.url_for_proxy+country+"/")
			## Change per page to show max records
			# form_select_option(self.browser, 'xpp', '5')
			self.execute_script(self.browser, "document.getElementById(\'xpp\').options[5].selected = true;")
			# self.execute_script(self.browser, "document.getElementById(\"xf2\").form.submit();")
			self.execute_script(self.browser, "document.getElementById(\'xf2\').options[1].selected = true;")
			self.execute_script(self.browser, "document.getElementById(\"xpp\").form.submit();")
			self.proxies.append({'country': country, 'proxies': self.read_proxies()})
			# self.sleep_script(1)
			print('Read proxies from'+ country+ ', continuing...')
		return self.proxies

	def read_as_soup(self, browser):
		allHTML = BeautifulSoup(browser.page_source)
		html=allHTML.encode('utf-8')
		return BeautifulSoup(html, 'html.parser')

	def execute_script(self, browser, script):
		browser.execute_script(script)
		sleep_script()
		return True

	def get_site_captcha_key(self):
		try:
			return self.browser.find_element_by_xpath('//div[@class=\"g-recaptcha\"]').get_attribute('data-sitekey')
		except Exception as e:
			return False

	def open_url(self, browser, url):
		print("Loading "+ str(url))
		# time.sleep(30)
		repeat = False
		while not repeat:
			try:
				browser.get(url)
				self.sleep_script()
				repeat = True
			except:
				print("Something went wrong loading the requested page, trying again!")
				repeat = False
				self.sleep_script(1)
		print("Page loaded successfully")
		return True

	def sleep_script(self, seconds='normal'):
		if seconds == 'normal':
			time.sleep(90.0/1000.0)
			return
		else:
			time.sleep(seconds)
			return

	def form_input_text(self, browser, selector, val, js=False, index=False):
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
			self.sleep_script()
			# print("Executing script"+ script)
			browser.execute_script(script)
		self.sleep_script()
		return True

	"""
	Selecting an option from the supplied select options parent
	jQuery(".bootstrap-select.beds").find('li a span:contains(1.0)').parent().trigger("click")
	"""
	def form_select_option(self, browser, jQuerySelector, val_to_select):
		script = "jQuery(\"%s\").val(\'%s\');" % (jQuerySelector, val_to_select)
		script += "jQuery(\""+ jQuerySelector +"\").trigger(\'change\');"
		self.sleep_script()
		browser.execute_script(script)
		self.sleep_script()
		return True

	"""
	Select checkbox
	jQuery("#hideContact").prop('checked', true)
	"""
	def form_select_checkbox(self, browser, selector, js=False):
		if not js:
			self.sleep_script()
			# script = "jQuery(\"%s\").prop('checked', true)" % (selector)
			# browser.execute_script(script)
			browser.find_element_by_id(selector).click()
			self.sleep_script()
			return True
		if not index:
			script = "jQuery(document).find(\""+ selector +"\").prop('checked', true);"
			script += "jQuery(document).find(\""+ selector +"\").trigger(\'change\');"
		else:
			script = "jQuery('"+ selector +"').eq(\'"+str(index)+"\').prop('checked', true);"
			script += "jQuery('"+ selector +"').eq(\'"+str(index)+"\').trigger(\'change\');"
		self.sleep_script()
		# print("Executing script"+ script)
		browser.execute_script(script)
		return True

	def execute_script(self, browser, script):
		browser.execute_script(script)
		self.sleep_script()
		return True

	def read_proxies(self):
		proxies = []
		html = self.read_as_soup(self.browser)
		target_table = html.find_all('table')[1].find('table')
		# target_table = target_outer_table
		i=0
		for row in target_table.find_all('tr', class_=re.compile("spy1x")):
			try:
				proxy = row.find('td').text.split('document.write')[0].split(" ")[1]
				port = row.find('td').text.rsplit(":", 1)[1]
				print("Proxies read:")
				print(proxy + ":" + port)
				proxies.append({'ip': proxy, 'port': port})
			except Exception as e:
				print("Error reading proxies!")
			# self.sleep_script(3)
		return proxies