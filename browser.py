import csv
from os import listdir
# from bs4 import BeautifulSoup
# import requests as req
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
# from config import _loginInput, _pwdInput, _loginButton, _username, _password, _xPathSearchBar, _xPathSearchButton, _xPathWait, _xPathDisplayMore
#import Image as Img




class Browser:
    
    def __init__(self, url):
        print("initiazing browser...")
        self.options = webdriver.ChromeOptions()
        self.updateURL(url)



    def start(self):
        self.browser = webdriver.Chrome(executable_path=r"C:\Users\user\Desktop\python\job\chrome.exe")
        # self.browser = webdriver.Chrome(chrome_options=self.options)#chrome_options=options
        self.browser.implicitly_wait(30)
        print("starting browser...")
        self.browser.get(self.url)

    def changeSite(self, url):
        self.browser.get(url)


    def find_elements(self,xpath,xPath):
        return self.browser.find_element(xpath,xPath)

    def updateURL(self, url):
        self.url = url
    

    def rollPages(self): #add
        for x in range(1,11,2):
            time.sleep(0.5)
            j=x/10
            js="document.documentElement.scrollTop=document.documentElement.scrollHeight * %s"%j
            return self.browser.execute_script(js)


    def getDriver(self):  #add
        return self.driver


    def clickOnElement(self,xpath,xPath):
        element = self.browser.find_element(xpath,xPath)    
        element.click()


    def clickOnElementbyLinkTxt(self,text): #add ok
        element = self.browser.find_element(text)    
        element.click()

    def clickOnElementbyClass(self,className,classname): #add ok
        element = self.browser.find_element(className,classname)    
        element.click()

    def clickOnElementbyPLinkTxt(self,text): #add ok
        element = self.browser.find_element(text)    
        element.click()

    

    def enterInInput(self,xPath, text):
        element = self.browser.find_element(xPath)
        element.send_keys(text)
    
    def addOption(self, option):
        self.options.add_argument(option)

    def defaultOptions(self):
        self.options.add_argument('headless')
        self.options.add_argument('window-size=1920x1080')
        self.options.add_argument("disable-gpu")

    def readTheElement(self,xpath,xPath):
        element = self.browser.find_element(xpath,xPath)
        return element.text

    def readTheElementBytag(self,tag):
        element = self.browser.find_element(tag)
        return element.text

    def readTheElementsByClass(self,classname): #add ok
        element = self.browser.find_elements(classname)
        return element


    def readTheElementByClass(self,classname): #add ok
        element = self.browser.find_element_by_class_name(classname)
        return element.text

    def readTheElementByLTxt(self,ltxt): #add ok
        element = self.browser.find_element(ltxt)
        return element.text

    def readTheElementLink(self,css):
        element = self.browser.find_element(css)
        return element.get_attribute('href')

    def readTheElementscssselec(self,css): #add
        element = self.browser.find_elements(css)
        return element
        # return element
        # lis =self.browser.find_element(csss)
        # for li in lis:
        #     name=li.find_element(css).text
        # return name




    def readTheElementcssselec(self,css):
        element = self.browser.find_element(css)
        return element.text

    def getNextPage(self,xPath): #add
        element = self.browser.find_element(xPath)    
        for i in range(1,500):
            return element.click()

    def scanNextPage(self): #add   
        for page in range(2,1000):
            return self.browser.get(self.url+"&p="+str(page))



# if len(next_page)==0 or next_page[0]==”#” :
#     return “finish”
# else:
#     return search(“http:”+next_page[0])


    # def Soup(self):
    #     soup = BeautifulSoup(self.browser.page_source, "html.parser")
    #     return self.soup

    # def useSoup(self,x):
    #     self.soup.find_all(x)

    # def useSoupforId(self,x):
    #     self.soup.find_all(id=x)



    def loginToSite(self, loginInput, pwdInput, loginButton, username, password):
        self.enterInInput(loginInput,username)
        self.enterInInput(pwdInput, password)
        self.clickOnElement(loginButton)
        
    def inputToSiteSearchBar(self,xPathToBar, clause, xPathConfirmButton):
        self.enterInInput(xPathToBar, clause)
        self.clickOnElement(xPathConfirmButton)


    def openFileToRead(self,filename):
        return open(filename, "r").read()

    def startScan(self):
        self.start()
        print("proceeding with login...")
        self.clickOnElement('//*[@id="toolbar"]/div/div[3]/div/div/div[1]/div/img')
        self.loginToSite(_loginInput, _pwdInput, _loginButton, _username, _password)
        self.inputToSiteSearchBar(_xPathSearchBar, self.openFileToRead("sateliteSetup.txt"), _xPathSearchButton)
        print(self.readTheElement(_xPathWait))
        self.checkWhatNeedDownload()

        try:
            for n in range(int(self.readNoOfPages())):
                self.clickOnElement(_xPathDisplayMore)
                while self.readTheElement(_xPathWait) == "Loading…":
                    pass
                self.checkWhatNeedDownload()

        finally:
            self.browser.close()




    def readNoOfPages(self):
        return self.readTheElement('//*[@id="list-container"]/div/div[4]/div/span[5]')[3:]

    def readCurrentPage(self):
        return self.readTheElement('//*[@id="page-selector"]')



    def goBack(self):  #add
        self.browser.back()
    

    def loadDownloadedImageNames(self):
        images = set()
        lister = listdir('../../downloadFromSatellite')
        for entry in lister:
            images.add(Img.Image(entry))
        for row in self.tsvReader():
            if len(row) > 1:
                images.add(Img.Image(row[0]))
        return images

    def checkWhatNeedDownload(self):
        ownedImages = self.loadDownloadedImageNames()
        for entryNo in range(1, 16):
            makeXPath = '//*[@id="product-list"]/div/div/div[' + str(
                entryNo) + ']/div/div/div/div[1]/div/div[1]/div/div'
            newImageEntry = Img.Image(self.readTheElement(makeXPath))
            if (newImageEntry.getSourceSatelite() == "S2A"):
                if (newImageEntry.getProductType() == "MSIL2A"):
                    downloadSemafor = True
                    for image in ownedImages:
                        if (newImageEntry.getDate() == image.getDate()):
                            downloadSemafor = False
                            break
                    if (downloadSemafor):
                        print("Starting download")
                        makeXPathDownload = '   //*[@id="product-list"]/div/div/div[' + str(
                            entryNo) + ']/div/div/div/div[1]/div/div[2]/div/div[2]/div[1]/a'
                        self.saveURLsToDownload(self.readTheElement(makeXPath), self.readTheElement(makeXPathDownload))

    def saveURLsToDownload(self, name, url):
        with open("toDownload.txt", "at") as outFile:
            tsvWriter = csv.writer(outFile, delimiter="\t")
            tsvWriter.writerow([name, url])

    def saveSiteResult(self, shopName,fieldname,items):   #add
        with open(shopName + ".csv","ab", encoding="utf-8") as outFile:             #need to add timestamp to filename
            tsvWriter = csv.DictWriter(outFile,fieldname, delimiter = "\t")
            tsvWriter.writeheader()
            tsvWriter.writerow(items)
            # for item in items:
            #     tsvWriter.writerow(item)  
    # #where item is ["name", "price", "whatever"]
    # #list of iteams = [["name", "price", "whatever"],["name", "price", "whatever"],["name", "price", "whatever"]]
    # #for a,b,c in price, name, potato:
    # # listOfIteams.append([a,b,c])


    # def momotest(self):
    #     lis=self.browser.find_element_by_css_selector("div.prdListArea")
    #     for li in lis:
    #         name=li.find_element_by_css_selector( 'a p.prdName').text
    #         print(name)
            




      # def saveSiteResult(self, shopName,fieldnames, listOfThings):
      #   with open(shopName + ".txt", "at") as outFile: #need to add timestamp to filename
      #       tsvWriter = csv.DictWriter(outFile,fieldnames, delimiter = "\t")
      #       tsvWriter.writeheader()
      #       for item in listOfThings:
      #           tsvWriter.writerow(item)  




#option類別產生實體
    def get_options():
        chrome_options=Options()
        chrome_options.add_argument("--headless")







    def tsvReader(self):
        this = []
        with open("toDownload.txt", "r") as inFile:
            tsvWriter = csv.reader(inFile, delimiter="\t")
            for row in tsvWriter:
                this.append(row)
            return this



    def close(self):
        self.browser = webdriver.Chrome(chrome_options=self.options)#chrome_options=options
        print("closing browser...")
        self.browser.quit()




    


    
