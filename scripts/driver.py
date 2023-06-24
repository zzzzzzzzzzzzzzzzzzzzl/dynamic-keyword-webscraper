from selenium import webdriver
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from scripts.fileManager import *
from scripts.functions import *
from urllib.parse import urlparse, urlunparse
import time
from scripts.tree import *
from scripts.outputData import *
import random


class driver:
    def __init__(self, data, protocal, idx, branchSize=100, timeOutAfter=1000) -> None:
        self.idx = idx
        self.driver = self.configDriver()
        self.keywords = [
            prepareString(word) for word in fileManager("keywords.json").loadData()
        ]
        self.wildCards = [
            word[1:]
            for word in list(filter(lambda word: word.startswith("*"), self.keywords))
        ]

        self.keywords = list(
            filter(lambda word: not word.startswith("*"), self.keywords)
        )

        self.tree = tree(branchSize)
        self.startTime = time.time()
        self.timeOutAfter = timeOutAfter
        self.timeout = False
        self.link = data[0]
        self.protocal = protocal
        self.data = data

        self.visitedUrls = []
        self.textWithKeyWords = []
        self.internalLinks = []
        self.failedToGetUrl = []

        self.newDomain(self.link)
        self.getPageData(self.domain)
        time.sleep(1)

    def scrapeDomain(self):
        self.iterateThroughInternalLinks()
        self.close()

        if self.textWithKeyWords:
            outputData(
                self.data,
                self.domain,
                self.textWithKeyWords,
                self.keywords,
            )

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
        try:
            self.driver.get(self.protocal + url)
            self.domain = self.protocal + url
        except:
            print("failed to get url")

        self.parseHtml()

    def openUrl(self, url):
        self.url = url
        self.visitedUrls.append(url)
        try:
            self.driver.get(url)
            self.parseHtml()
            return True

        except:
            print("failed to get url")
            self.failedToGetUrl.append(url)
            return False

    def parseHtml(self):
        self.soup = BeautifulSoup(self.driver.page_source, "html.parser")
        self.soup.prettify()

    def keyWordDictGen(self):
        dict = {}
        for i in self.keywords + self.wildCards:
            dict[i] = False
        return dict

    def findTextWithKeyword(self):
        keywordDict = self.keyWordDictGen()
        textWithKeyword = []
        textWithKeyword
        tagFilter = ["style", "script", "iframe"]
        for i in self.soup.findAll():
            if i.name not in tagFilter:
                found = []
                for word in str(i.text).lower().split(" "):
                    for keyword in self.keywords:
                        if keyword == word:
                            found.append(keyword)
                            keywordDict[keyword] = True
                    for wildCard in self.wildCards:
                        if word.startswith(wildCard):
                            found.append(wildCard)
                            keywordDict[wildCard] = True
                            append = True

                if found:
                    for j in textWithKeyword:
                        if i.text in j["text"]:
                            textWithKeyword.remove(j)
                    textWithKeyword.append(
                        {"text": i.text, "keyword": found, "html": self.soup.prettify()}
                    )

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
                and "#" not in href
                and "=" not in href
                and "%" not in href
                and "&" not in href
                and "+" not in href
                and ":" not in href.replace("://", "")
            ):
                url = self.getFullUrl(href)
                if url == True:
                    pass
                elif url not in self.internalLinks:
                    if "https" in url[4:]:
                        a, b = chopchop(url)
                        internalLinks.append(a)

                    else:
                        internalLinks.append(url)

        self.internalLinks = self.internalLinks + internalLinks

    def sortInternalLinks(self):
        self.internalLinks = list(set(self.internalLinks))
        self.internalLinks = [
            i for i in self.internalLinks if i not in self.visitedUrls
        ]
        self.internalLinks = sorted(self.internalLinks, key=lambda x: len(x.split("/")))

    def getPageData(self, url):
        goturl = self.openUrl(url)

        self.findTextWithKeyword()
        self.getInternalLinks()
        return goturl

    def iterateThroughInternalLinks(self):
        recusions = 0
        while self.internalLinks:
            self.getRunTime()
            if self.timeout:
                print("timeout")
                break
            recusions += 1
            self.getPageData(self.internalLinks[0])
            if self.internalLinks:
                self.visitedUrls.append(self.internalLinks[0])
                if self.internalLinks:
                    print(
                        "idx  :",
                        self.internalLinks[0],
                        "recursion  :",
                        recusions,
                        "links :",
                        len(self.internalLinks),
                    )
            self.internalLinks.pop(0)
            self.sortInternalLinks()

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
