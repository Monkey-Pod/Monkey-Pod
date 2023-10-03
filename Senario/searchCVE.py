from bs4 import BeautifulSoup
from urllib import request


def searchCVE():
    cve_lists = ["CVE-2019-11043","CVE-2011-2523","CVE-2022-kokoaerg"]

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


        """
        url = "https://twitter.com/search?q=" + i + "%20PoC&src=typed_query&f=top"
        print(url)
        response = request.urlopen(url)
        soup = BeautifulSoup(response,"html.parser")
        response.close()
        
        hitNum = soup.find("span",class_="css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0")
        if not ("No results" in hitNum.text):
            if(alreadyPutLabel == 0):
                alreadyPutLabel = 1
                print("===============")
                print(i)
                print("===============")

            print(url)
            """ 

searchCVE()
