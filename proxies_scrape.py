from scraping_helpers import *

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
	browser = None
	proxies = []
	tier_1_countries_test = ['AU', 'AT', 'BE', 'CA', 'CO', 'HR', 
		 	 'CZ', 'DK', 'FI', 'GE', 'DE', 'IE', 
		 	 'IL', 'IT', 'KR', 'LT', 'LU', 'MK', 
		 	 'MU', 'NL', 'NZ', 'NI', 'NO', 'PL',
		 	 'SK', 'SI', 'ES', 'TW', 'GB', 'US']
	tier_1_countries = ['AU', 'AT',]

	def get_browser(self):
		return self.browser

	def init_browser(type='firefox', options={'headless': False, 'maximize_window': True}, profile=False):
		## Initialize Firefox browser
		# options = Options()
		# options.add_argument("--headless")
		# browser = webdriver.Firefox(firefox_options=options)
		print("Call received inside init_browser"+ profile)
		if profile == False:
			print("COntinuing without proxy")
			browser = webdriver.Firefox()
		else:
			print("Setting profile for firefox")
			browser = webdriver.Firefox(firefox_profile=profile)
		# 	browser = webdriver.Firefox(profile)
		## Maximize window and open the base url
		browser.maximize_window()
		return browser

	def __init__(self, proxy=False, port=False):
		print("Init called")
		# print("Proxy:"+ proxy + " Port:"+ port)
		# if not proxy:
		# 	self.browser = self.init_browser('firefox', {'headless': False, 'maximize_window': True})
		# else:
		# 	print("Setting up proxxy")
		# 	# self.set_proxy(proxy, port)
		# 	self.browser = self.init_browser('firefox', {'headless': False, 'maximize_window': True})

	def set_proxy(self, ip, port):
		profile = webdriver.FirefoxProfile()
		profile.set_preference("network.proxy.type", 1)
		profile.set_preference("network.proxy.http", ip)
		profile.set_preference("network.proxy.http_port", port)
		profile.set_preference("network.proxy.ssl", ip)
		profile.set_preference("network.proxy.ssl_port", port)
		# self.browser = webdriver.Firefox(firefox_profile=profile)
		self.browser = self.init_browser('firefox', {'headless': False, 'maximize_window': True}, profile)
		return self.browser

	def browse_url(self, browser, url):
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

	def process_proxies(self):

		for country in self.tier_1_countries:
			print('Working with'+ country)
			open_url(self.browser, self.url_for_proxy+country+"/")
			## Change per page to show max records
			# form_select_option(self.browser, 'xpp', '5')
			execute_script(self.browser, "document.getElementById(\'xpp\').options[5].selected = true;")
			# execute_script(self.browser, "document.getElementById(\"xf2\").form.submit();")
			execute_script(self.browser, "document.getElementById(\'xf2\').options[1].selected = true;")
			execute_script(self.browser, "document.getElementById(\"xpp\").form.submit();")
			self.proxies.append({'country': country, 'proxies': self.read_proxies()})
			# sleep_script(1)
			print('Read proxies from'+ country+ ', continuing...')
		return self.proxies

	def open_url(self, url):
		open_url(self.browser, url)

	def read_proxies(self):
		proxies = []
		html = read_as_soup(self.browser)
		target_table = html.find_all('table')[1].find('table')
		# target_table = target_outer_table
		i=0
		for row in target_table.find_all('tr', class_=re.compile("spy1x")):
			try:
				proxy = row.find('td').text.split('document.write')[0].split(" ")[1]
				port = row.find('td').text.rsplit(":", 1)[1]
				print("Proxy and port read==")
				print(proxy + ":" + port)
				proxies.append({'ip': proxy, 'port': port})
			except Exception as e:
				print('Exception')
				print(e)
			# sleep_script(3)
		return proxies