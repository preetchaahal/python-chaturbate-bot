import random
import sys
import time
from faker import *
from db_helpers import *
from proxies_scrape import *
from recaptcha_api_v2 import *

"""
Bot to generate fake creds for chaturbate.com

Fake creds include
1. username
2. password
3. email
4. dob
5. gender

#Step 1 
- Generate fake creds

#Step 2
- Save in DB

#Step 3
- Begin registration per DB record
- Read proxies and perform registration by switching between the read proxies

"""

print("Initializing Chaturbate-Random-Registration Bot v0.09")
proxies = []
web = Proxy(False)
web.log('info', 'Starting **Chaturbate Random Registration Bot**')
web.log('info', 'Reading proxies')
web.process_proxies()
proxies = web.proxies

print("proxies")
print(proxies)
print("Generating users")
web.log('info', 'Generating users with dummy data')
db = DbConn()
max_limit = db.user_limit

faker = Faker()
data_sets = faker.generate_data(max_limit)

counter = 0
for data_set in data_sets:
	if counter == max_limit:
		break
	db.insert('users', data_set)
	counter += 1

print("Fetching data")
users = db.select("users", True, "status = False")

browser = web.get_browser()

web.log('info', 'Read %s proxies' % len(proxies))
proxy_set = []
for prox in proxies:
	i = 0
	for prox_inner in prox['proxies']:
		if i == 0:
			i += 1
			continue
		proxy_set.append({'ip': prox_inner['ip'], 'port': prox_inner['port']})
		web.log('info', 'IP: %s PORT: %s' % (prox_inner['ip'], prox_inner['port']))

print("Closing existing open window")
web.close_browser()

# users = ['abc']
# 94.177.238.131:8080
# 182.253.201.76:10000


web.log('info', 'Starting account registration process on chaturbate.com')

# for i in range(len(users)):
i = 0
while i < len(users):
	web.log('info', '***********************')
	if i < 0:
		i = 0
	user = users[i]

	# After every 40 users re-load proxies
	if i % 2 == 0 and i > 0:
		print("Re-load proxies")
		web.log('info', 'Reading proxies')
		web.process_proxies()
		proxies = web.proxies
		print("proxies")
		print(proxies)

		web.log('info', 'Read %s proxies' % len(proxies))
		proxy_set = []
		for prox in proxies:
			i = 0
			for prox_inner in prox['proxies']:
				if i == 0:
					i += 1
					continue
				proxy_set.append({'ip': prox_inner['ip'], 'port': prox_inner['port']})
				web.log('info', 'IP: %s PORT: %s' % (prox_inner['ip'], prox_inner['port']))

	print("Working with user: i="+ str(i))
	print(user)
	# user = {'username': 'preet321098', 'password': 'ajdb53$asn!20', 'email': 'preet321098@gmail.com', 'dob': '3-4-1992', 'gender': 'm'}
	current_proxy = random.choice(proxy_set)
	# current_proxy = {'ip': '36.67.41.125', 'port': 80}
	# web = Proxy(False)
	print("Attempting with proxy")
	print(current_proxy)
	web = Proxy({'ip': current_proxy['ip'], 'port': current_proxy['port']})
	web.log('info', 'Attempting browser session with IP: %s PORT: %s' % (current_proxy['ip'], current_proxy['port']))
	
	# web = Proxy()
	# web.set_proxy_profile(current_proxy['ip'], current_proxy['port'])
	# web.set_proxy_profile(current_proxy['ip'], current_proxy['port'])
	# web.init_browser('firefox', {'headless': False, 'maximize_window': True}, current_proxy)
	
	browser = web.get_browser()
	
	# print("Attempting proxy"+ current_proxy['ip'] + ":" + current_proxy['port'])
	# if not web.browse_url("https://ipinfo.info/html/ip_checker.php"):
	# 	web.close_browser()
	# 	i -= 1
	# 	continue
	# time.sleep(1)
	# print("Exiting")
	# web.browser.close()
	# continue
	# Web Scraping
	URL_REGISTER = "https://chaturbate.com/accounts/register/"
	# Scraping in case of single user
	web.browse_url(URL_REGISTER)

	# Check if captcha page encountered
	page_blocked_by_captcha = web.is_page_blocked_by_captcha()
	if page_blocked_by_captcha:
		print(web.is_page_blocked_by_captcha())
		print("Restarting the operation...")
		i = i - 1
		web.close_browser()
		web.log('error', 'Failed to perform registration with IP: %s PORT: %s, restarting with a different proxy configuration.' % (prox_inner['ip'], prox_inner['port']))
		continue

	## Working with re-captcha
	captcha_site_key = web.get_site_captcha_key()
	if not captcha_site_key:
		i = i - 1
		web.close_browser()
		print("Unable to find google captcha key, switching proxy")
		web.log('error', 'Re-Captcha key not found, restarting wuth a  different proxy configuration')
		continue

	print("Auto-filling details")

	web.log('info', 'Registration under way...')
	web.log('info', 'Re-Captcha key: %s' % (captcha_site_key))
	print("Re-Captcha key")
	print(captcha_site_key)

	api = RecaptchaAPI(captcha_site_key)
	web.log('info', 'Re-Captcha auto-solve requested')

	if not web.is_jQuery_rendered_completely():
		print("Page not loaded completely, restarting the operation...")
		i = i - 1
		web.close_browser()
		web.log('error', 'Failed to perform registration with IP: %s PORT: %s, restarting with a different proxy configuration. Page didnt load up completely ' % (prox_inner['ip'], prox_inner['port']))
		continue


	web.form_input_text(browser, "input[name=\'username\']", user['username'], True)
	web.form_input_text(browser, "input[name=\'password\']", user['password'], True)
	web.form_input_text(browser, "#id_email", user['email'], True)

	dob_set = user['dob'].split('-')
	web.form_select_option(browser, "select[name=\'birthday_month\']", dob_set[0])
	web.form_select_option(browser, "select[name=\'birthday_day\']", dob_set[1])
	web.form_select_option(browser, "select[name=\'birthday_year\']", dob_set[2])

	web.form_select_option(browser, "select[name=\'gender\']", user['gender'])

	web.form_select_checkbox(browser, 'id_terms')
	web.log('info', 'Form filled with Username: %s, Password: %s, Email: %s, DOB: %s, Gender: %s' % (user['username'], user['password'], user['email'], dob_set, user['gender']))
	web.log('info', 'Requesting Re-captcha response')
	captcha_solved = api.get_response()
	web.log('info', ['Re-captcha response:', captcha_solved])
	web.form_input_text(browser, "textarea[id=\'g-recaptcha-response\']", captcha_solved['solution']['gRecaptchaResponse'], True)
	web.execute_script(browser, "document.getElementsByTagName(\'form\')[1].submit();")
	web.log('info', 'Attempting registration')
	time.sleep(10)
	print("Registration successful")
	web.log('info', 'Registration successful')
	web.log('info', '***********************')
	web.close_browser()
	db.update("users", "status = %s" % True, "id=%s" % user['id'])
	print("Attempting registration...")
	i += 1

print("END of Script")