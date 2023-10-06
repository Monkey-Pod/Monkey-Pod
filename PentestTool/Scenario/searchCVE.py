#!/usr/bin/env python3

from bs4 import BeautifulSoup
from urllib import request

def searchCVE(cve):
    cve_lists = cve
    for i in cve_lists:
        url = "https://github.com/search?q="+ i +"+exploit&type=repositories"
        alreadyPutLabel = 0
        response = request.urlopen(url)
        soup = BeautifulSoup(response,"html.parser")
        response.close()
        hitNum = soup.find("div",class_="Box-sc-g0xbh4-0 cgQapc")
        if not ("0 results" in hitNum.text):
            if(alreadyPutLabel == 0):
                alreadyPutLabel = 1
                print("===============")
                print(i)
                print("===============")
            print(hitNum.text)
            print(url)


