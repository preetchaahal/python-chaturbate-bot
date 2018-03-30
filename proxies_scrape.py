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

	def __init__(self):
		self.browser = init_browser('firefox', {'headless': False, 'maximize_window': True})

	def process_proxies(self):
		for country in self.tier_1_countries:
			print('Working with'+ country)
			open_url(self.browser, self.url_for_proxy+country+"/")
			## Change per page to show max records
			# form_select_option(self.browser, 'xpp', '5')
			execute_script(self.browser, "document.getElementById(\'xpp\').options[5].selected = true;")
			execute_script(self.browser, "document.getElementById(\"xpp\").form.submit();")
			self.proxies.append({'country': country, 'proxies': self.read_proxies()})
			# sleep_script(1)
			print('Read proxies from'+ country+ ', continuing...')
		return self.proxies

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