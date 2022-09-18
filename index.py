import re
import time
import json
from ast import Try
from bleach import clean
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from concurrent.futures.thread import ThreadPoolExecutor
from selenium.webdriver.support import expected_conditions as EC

class ScrapingPortalJob:
    html = ""
    profile = ''
    listJobs = []
    CLEANR = re.compile('<.*?>')
    linkPortalJob = "https://id.indeed.com"
    driver = webdriver.Chrome('C://Users//praka//Downloads//chromedriver.exe')

    def __init__(self):
        self.driver.get(self.linkPortalJob)
        time.sleep(3)

    def __getPage(self, url):
        page = requests.get(url)

        if page.status_code == 200:
            soup = BeautifulSoup(page.content, "html.parser")

            return soup
        else:
            return ""

    def typingWhat(self):
        this = self
        elemInput = this.driver.find_element(By.ID, "text-input-what")
        elemInput.send_keys("marketing")

    def typingWhere(self):
        this = self
        elemInput = this.driver.find_element(By.ID, "text-input-where")
        elemInput.send_keys("jakarta")

    def clickFindJob(self):
        this = self
        btn = this.driver.find_element(By.CLASS_NAME, "yosegi-InlineWhatWhere-primaryButton")
        btn.click()

    def __getDescJob(self, link):
        getPageJobs = self.__getPage(link)
        listDesc = getPageJobs.select("#jobDescriptionText")[0]
        cleantext = re.sub(self.CLEANR, '',str(listDesc))
        print(cleantext)
        return cleantext

    def fetchData(self):
        this = self
        print("loading...")
        try:
            this.html = WebDriverWait(this.driver, 30).until(
                EC.presence_of_element_located((By.ID, "pageContent"))
            )
        finally:
            soup = BeautifulSoup(this.html.get_attribute('innerHTML'), "html.parser")
        try:
            if len(soup.select(".mosaic-zone")[1]) > 0:
                for data in soup.select(".mosaic-zone")[1].select("div > a"):
                    title = data.select(".jobTitle > span")[0]
                    compName = data.select(".companyName")[0]
                    companyLocation = data.select(".companyLocation")[0]
                    linkJob = this.linkPortalJob + data.get("href")
                    descJob = this.__getDescJob(linkJob)

                    jobs = {
                        "title" : title.text,
                        "compName" : compName.text,
                        "companyLocation" : companyLocation.text,
                        "linkJob" : linkJob,
                        "descjob" : descJob,
                    }

                    this.listJobs.append(jobs)
        except Exception as e:
            print(e)

        dumpListJobs = json.dumps(this.listJobs)
        writeJobs = open("jobs.json", 'w')
        writeJobs.write(dumpListJobs)

        print("DONE!")

    def readFileJobs(self):
        readJobs = open("jobs.json", 'r')
        loadReadJobs = json.load(readJobs)

        print(len(loadReadJobs))

ScrapingPortalJob = ScrapingPortalJob()
ScrapingPortalJob.typingWhat()
ScrapingPortalJob.typingWhere()
ScrapingPortalJob.clickFindJob()
time.sleep(3)
ScrapingPortalJob.fetchData()





