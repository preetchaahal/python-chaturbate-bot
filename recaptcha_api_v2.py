import time
from python3_anticaptcha import NoCaptchaTaskProxyless

class RecaptchaAPI:
	ANTICAPTCHA_KEY = "ff687bda7bc0069cf0ebdf984f5bed82" 

	# G-ReCaptcha site key. Website google key. 
	SITE_KEY  =  '6Lf93goUAAAAAJKhC4y-Ok88s72iUJ8UX4bLQMmw' 

	# Link to a page with a cap. Page url. 
	PAGE_URL  =  'https://chaturbate.com/accounts/register/' 

	user_answer = None

	def __init__(self, site_key=None, page_url=None):
		# self.set_anticaptcha_key = anticaptcha_key
		if not site_key:
			site_key = self.SITE_KEY
		self.set_site_key(site_key)
		self.process_reptcha_request()

	def get_anticaptcha_key(self):
		return self.ANTICAPTCHA_KEY

	def get_site_key(self):
		return self.SITE_KEY

	def get_page_url(self):
		return self.PAGE_URL

	def set_anticaptcha_key(self, key=None):
		if key == None:
			self.ANTICAPTCHA_KEY = key

	def set_site_key(self, key=None):
		self.SITE_KEY = key

	def set_page_url(self, url=None):
		if url == None:
			self.PAGE_URL = url

	def process_reptcha_request(self):
		# self.user_answer = NoCaptchaTaskProxyless(anticaptcha_key = self.ANTICAPTCHA_KEY).captcha_handler(websiteURL=self.PAGE_URL, websiteKey=self.SITE_KEY)
		# self.
		self.user_answer = NoCaptchaTaskProxyless.NoCaptchaTaskProxyless(anticaptcha_key = self.ANTICAPTCHA_KEY).captcha_handler(websiteURL=self.PAGE_URL, websiteKey=self.SITE_KEY)
		return self.user_answer

	def get_response(self):
		print("Requesting response in "+ str(30) + " seconds...")
		time.sleep(30)
		self.process_reptcha_request()
		print("Response received from API")
		print(self.user_answer)
		return self.user_answer