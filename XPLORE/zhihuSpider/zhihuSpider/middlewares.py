# Importing base64 library because we'll need it ONLY in case if the proxy we are going to use requires authentication
# import base64
# Start your middleware class

import random
from djangoWorker.models import ProxyItem

class ProxyMiddleware(object):
    def __init__(self):
        self.proxies = ProxyItem.objects.all()

    # overwrite process request
    def process_request(self, request, spider):
        # Set the location of the proxy
        proxy = random.choice(self.proxies)

        request.meta['proxy'] = "http://" + proxy.ip + ":" + proxy.port
        print("----in proxy middleware ---")
        print(request.meta['proxy'])
        # # Use the following lines if your proxy requires authentication
        # proxy_user_pass = "USERNAME:PASSWORD"
        # # setup basic authentication for the proxy
        # encoded_user_pass = base64.encodestring(proxy_user_pass)
        # request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass