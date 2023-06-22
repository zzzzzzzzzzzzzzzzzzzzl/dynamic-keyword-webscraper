from selenium import webdriver
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from scripts.fileManager import *
from scripts.functions import *
from urllib.parse import urlparse, urlunparse
import time
from scripts.tree import *
from scripts.outputData import *


class driver:
    def __init__(self, data, idx, branchSize=100, timeOutAfter=1000) -> None:
        self.idx = idx
        self.driver = self.configDriver()
        self.keywords = [
            prepareString(word) for word in fileManager("keywords.json").loadData()
        ]
        self.tree = tree(branchSize)
        self.startTime = time.time()
        self.timeOutAfter = timeOutAfter
        self.timeout = False
        self.link = data[0]

        self.visitedUrls = []
        self.textWithKeyWords = []
        self.internalLinks = []
        self.failedToGetUrl = []

        self.data = data
        self.newDomain(self.link)
        self.getPageData(self.domain)
        time.sleep(0.5)

    def scrapeDomain(self):
        self.iterateThroughInternalLinks()
        self.close()
        # duplicatetext = self.textWithKeyWords[:]
        # self.textWithKeyWords = removeDuplicateFromTextWithKeyWords(
        #     self.textWithKeyWords
        # )
        # if self.textWithKeyWords:
        #     outputData(
        #         self.textWithKeyWords,
        #         self.domain,
        #         self.data,
        #         self.keywords,
        #         duplicatetext,
        #     )
        print("saving")
        fileManager(f"{self.idx}.json", [self.textWithKeyWords, "testing"]).save()

    def getRunTime(self):
        if (time.time() - self.startTime) > self.timeOutAfter:
            self.timeout = True

    def getFullUrl(self, link):
        self.link = link
        branchFull = self.tree.addLink(link)
        if branchFull:
            return True
        return self.domain + link

    def newDomain(self, url):
        self.url = url
        print(self.url)

        try:
            self.driver.get("https://" + url)
            self.domain = "https://" + url
        except:
            self.driver.get("http://" + url)
            self.domain = "http://" + url

        self.parseHtml()

    def openUrl(self, url):
        if url not in self.visitedUrls:
            self.url = url

        # try:
        self.driver.get(url)
        self.parseHtml()
        self.visitedUrls.append(url)
        return True

    # except:
    #     print("failed to get url")
    #     self.failedToGetUrl.append(url)
    #     self.visitedUrls.append(url)
    #     return False

    def parseHtml(self):
        self.soup = BeautifulSoup(self.driver.page_source, "html.parser")

    # def findTextWithKeyword(self):
    #     textWithKeyword = {"text": [], "keywords": []}
    #     for keyword in self.keywords:

    #         def filterByKeyword(tag):
    #             return keyword in str(tag.string).lower()

    #         text = [text.string for text in self.soup.find_all(filterByKeyword)]
    #         if text:
    #             textWithKeyword = textWithKeyword + [
    #                 text.string for text in text
    #             ]
    #             textWithKeyword["keywords"] = textWithKeyword["keywords"] + [keyword]

    #     if textWithKeyword:
    #         self.textWithKeyWords = self.textWithKeyWords + [
    #             {
    #                 "textsWithKeyWords": [
    #                     textWithKeyword,
    #                     self.soup.prettify(),
    #                 ],
    #                 "page": self.url,
    #             }
    #         ]
    def keyWordDictGen(self):
        dict = {}
        for i in self.keywords:
            dict[i] = False
        return dict

    def findTextWithKeyword(self):
        keywordDict = self.keyWordDictGen()
        textWithKeyword = []
        tagFilter = ["style"]
        for i in self.soup.findAll():
            if i.name not in tagFilter:
                append = False

                for keyword in self.keywords:
                    if keyword in str(i.text).lower():
                        append = keyword
                        keywordDict[keyword] = True

                if append:
                    for j in textWithKeyword:
                        if i.text in j["text"]:
                            textWithKeyword.remove(j)
                    textWithKeyword.append({"text": i.text, "tag": i.name})

        if textWithKeyword:
            self.textWithKeyWords = self.textWithKeyWords + [
                {
                    "textsWithKeyWords": textWithKeyword,
                    "keywords": keywordDict,
                    "page": self.url,
                }
            ]

    def getInternalLinks(self):
        internalLinks = []
        for anchor in self.soup.find_all("a"):
            href = anchor.get("href")
            if (
                (not urlparse(href).netloc or self.domain in href)
                and href
                and " " not in href
                and "@" not in href
            ):
                url = self.getFullUrl(href)
                if url == True:
                    pass
                elif url not in self.internalLinks:
                    if "https" in url[4:]:
                        a, b = chopchop(url)
                        internalLinks.append(a)
                        internalLinks.append(b)
                    else:
                        internalLinks.append(url)

        self.internalLinks = self.internalLinks + internalLinks

    def getPageData(self, url):
        goturl = self.openUrl(url)
        if goturl:
            self.findTextWithKeyword()
            self.getInternalLinks()
            return goturl

    def iterateThroughInternalLinks(self, recusions=0):
        self.tree.saveTreeJson()
        self.getRunTime()
        if self.timeout:
            print(
                f"timeout",
            )
            return
        else:
            recusions += 1
            while self.internalLinks and not self.timeout:
                if self.internalLinks[0] not in self.visitedUrls:
                    goturl = self.getPageData(self.internalLinks[0])
                    if goturl:
                        print(
                            "idx  :",
                            self.internalLinks[0],
                            "recursion  :",
                            recusions,
                            "links :",
                            len(self.internalLinks),
                        )
                        self.iterateThroughInternalLinks(recusions)
                try:
                    self.internalLinks.pop(0)
                except:
                    print("list probably empty")

    def close(self):
        self.driver.quit()

    def configDriver(self):
        options = webdriver.ChromeOptions()

        options.add_argument("--headless")
        options.add_argument("--incognito")
        options.add_argument("--nogpu")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1280,1280")
        options.add_argument("--no-sandbox")
        options.add_argument("--enable-javascript")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        options.add_argument("--disable-blink-features=AutomationControlled")

        ua = UserAgent()
        userAgent = ua.random

        driver = webdriver.Chrome(options=options)
        driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )
        driver.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": userAgent})

        return driver
