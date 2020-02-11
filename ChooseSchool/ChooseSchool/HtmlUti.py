import urllib.request
import requests
class HtmlUtil:
    def __init__(self, url):
        self.url = url
        self.suffix = ""

    def changeUrl(self,url):
        self.url = url

    def setSuffix(self,suffix):
        self.suffix = suffix

    def getPage(self):
        req=urllib.request.Request(self.url+self.suffix)
        resp=urllib.request.urlopen(req)
        data=resp.read().decode('utf-8')
        return data
    
    def postPage(self,data):
        response = requests.post(self.url+self.suffix,data,headers={'Content-Type':'application/x-www-form-urlencoded'})
        return response.text