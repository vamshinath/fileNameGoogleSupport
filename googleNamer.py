from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from multiprocessing.dummy import Pool

options = Options()
options.headless = True 
files_count=0
counter=0
CHROMEDRIVER_PATH="/home/vamshi/chromedriver"
gotError=False

import requests,os,re,sys,shutil
import threading,time

def scanFiles():

    ofiles = {}
    imgFiles=[]

    for root, directories, filenames in os.walk('.'):
        for filename in filenames:
            if "9351" in filename or filename.startswith("gsd"):
                continue
            try:
                    f=os.path.abspath(os.path.join(root,filename))
                    fsz=os.stat(f).st_size
                    if fsz < 10240 or fsz > 4824000:
                        continue
                    ofiles[f]=fsz
            except Exception as e:
                print(e)

    files = sorted(ofiles.items(),key=lambda x:x[1],reverse=True)

    for fl,_ in files:
        flnm_lower=os.path.basename(fl.lower())
        if ".jpg" in flnm_lower or ".png" in flnm_lower or ".jpeg" in flnm_lower:
            imgFiles.append(fl)

    return imgFiles
 
def renameFile(fl,newName):
    if len(newName) <2:
        return

    path = os.path.dirname(fl)
    ext="."+os.path.basename(fl).split(".")[-1]
    shutil.move(fl,path+"/gsd"+newName+ext)
    print(fl,newName)

def getName(fl):
    
    global gotError

    try:
        searchUrl = 'https://smallseotools.com/reverse-image-search/'
        browser = webdriver.Chrome(CHROMEDRIVER_PATH,chrome_options=options)
    
        filePath = fl
        browser.get(searchUrl)
        time.sleep(2.5)

        browser.find_element_by_name("myfile").send_keys(filePath)

        time.sleep(10)

        browser.find_element_by_id("checkReverse").submit()

        imgname=googleAndYanex(browser)

        if imgname == False:
            print("Nothing")
            gotError = True
            return ""

        browser.close()
        return imgname.replace(" ",'_')
        
    except Exception as e:
        print("hey "+str(e))
        gotError = True
        browser.close()

    return ''

def getSLinks(browser):
    links=[]
    counter = 0
    while len(links) <3 and counter < 4:
        counter+=1
        try:
            links=browser.find_elements_by_link_text("Show Matches")
        except Exception as e:
            time.sleep(2.5)

    if len(links) < 3:
        return False

    return links

def getOtherContainerObject(browser):
    link=''
    counter = 0
    while ( link == '' or link == None) and counter < 4:
        counter+=1
        try:
            link=browser.find_element_by_class_name("other-sites__container")
        except Exception as e:
            time.sleep(2.5)

    if link == "" or link == None:
        return False

    return link

def googleAndYanex(browser):


    slinks=getSLinks(browser)
    yand=slinks[-1].get_attribute("href")

    try:
        imgname=getGoogleName(browser,slinks[0].get_attribute("href"))
    except Exception as e:
        print("googleAndYandex:"+e)
        imgname=''


    if imgname == None or len(imgname) < 3 :
        imgname = "yn"+getYandexName(browser,yand)
        print("Yandex")

    if imgname == None or len(imgname) < 3:
        return False 
    

    return imgname

def getGoogleName(browser,link):

    browser.get(link)
    time.sleep(2)
    imgname=browser.find_element_by_xpath('//*[@title="Search"]').get_attribute("value")

    return imgname


def getYandexName(browser,link):

    browser.get(link)
    time.sleep(2.5)

    ul=getOtherContainerObject(browser)
    if ul == False:
        return ""

    time.sleep(0.3)
    imgname=ul.find_element_by_class_name("other-sites__desc").text

    return imgname



def googleName(fl):

    return getName(fl)   



if __name__ == "__main__":
    googleName(sys.argv[1])
