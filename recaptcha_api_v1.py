import requests

"""
Complete API referecne:
`https://anticaptcha.atlassian.net/wiki/spaces/API/pages/5079089/NoCaptchaTask+Google+Recaptcha+puzzle+solving`

Sample API Request Object:
{
    "clientKey":"dce6bcbb1a728ea8d871de6d169a2057",
    "task":
        {
            "type":"NoCaptchaTask",
            "websiteURL":"http:\/\/mywebsite.com\/recaptcha\/test.php",
            "websiteKey":"6Lc_aCMTAAAAABx7u2N0D1XnVbI_v6ZdbM6rYf16",
            "proxyType":"http",
            "proxyAddress":"8.8.8.8",
            "proxyPort":8080,
            "proxyLogin":"proxyLoginHere",
            "proxyPassword":"proxyPasswordHere",
            "userAgent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
        }
}
"""

class Recaptcha_API:
    API_URI="http://api.anti-captcha.com/createTask"
    request_data = {
        "clientKey": "dce6bcbb1a728ea8d871de6d169a2057",
        "task":
        {
            "type":"NoCaptchaTask",
            "websiteURL":"http:\/\/mywebsite.com\/recaptcha\/test.php",
            "websiteKey":"6Lc_aCMTAAAAABx7u2N0D1XnVbI_v6ZdbM6rYf16",
            "proxyType":"http",
            "proxyAddress":"8.8.8.8",
            "proxyPort":8080,
            # "proxyLogin":"proxyLoginHere",
            # "proxyPassword":"proxyPasswordHere",
            "userAgent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
        }
    }
    r = None

    def __init__(self, url=None, type='get', data=None):
        if url == None:
            rq_url = self.API_URI
            # self.r = requests.get(self.API_URI)
        else:
            rq_url = url
            # self.r = requests.get(url)
        if data == None:
            data = self.request_data

        # if type == 'get':
        #     self.r = requests.get(rq_url, data=data)
        # else:
        #     self.r = requests.post(rq_url, data=data)
        self.r = requests.get(rq_url, data=self.request_data)

    def get_headers(self):
        return self.r.headers['content-type']

    def get_encoding(self):
        return self.r.encoding

    def get_response(self, type='text'):
        if type == 'text':
            return self.r.text

        if type == 'json':
            return self.r.json()