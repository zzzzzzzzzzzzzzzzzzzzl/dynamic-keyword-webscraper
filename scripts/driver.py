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
    def __init__(self, initialUrl, idx, branchSize=5, timeOutAfter=1000) -> None:
        self.idx = idx
        self.driver = self.configDriver()
        self.keywords = [
            prepareString(word) for word in fileManager("keywords.json").loadData()
        ]
        self.tree = tree(branchSize)
        self.startTime = time.time()
        self.timeOutAfter = timeOutAfter
        self.timeout = False

        self.visitedUrls = []
        self.textWithKeyWords = []
        self.internalLinks = []
        self.failedToGetUrl = []

        self.newDomain(initialUrl)
        self.getPageData(initialUrl)

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

    def scrapeDomain(self):
        self.iterateThroughInternalLinks()
        self.close()
        self.textWithKeyWords = removeDuplicateFromTextWithKeyWords(
            self.textWithKeyWords
        )
        if self.textWithKeyWords:
            outputData(self.textWithKeyWords, self.domain).updateOutputFile()
        # fileManager(f"{self.idx}.json", self.textWithKeyWords).save()

    def getRunTime(self):
        if (time.time() - self.startTime) > self.timeOutAfter:
            self.timeout = True

    def getFullUrl(self, link):
        branchFull = self.tree.addLink(link)
        if branchFull:
            return True
        return self.domain + link

    def newDomain(self, url):
        self.url = url
        self.driver.get(url)
        self.domain = self.getPageDomain(url)

        self.parseHtml()

    def getPageDomain(self, url):
        parsedUrl = urlparse(url)
        return parsedUrl.scheme + "://" + parsedUrl.netloc

    def openUrl(self, url):
        if url not in self.visitedUrls:
            self.url = url
            try:
                self.driver.get(url)
                self.parseHtml()
                self.visitedUrls.append(url)
                return True
            except:
                print("failed to get url")
                self.failedToGetUrl.append(url)
                self.visitedUrls.append(url)
                return False

    def parseHtml(self):
        self.soup = BeautifulSoup(self.driver.page_source, "html.parser")

    def findTextWithKeyword(self):
        textWithKeyword = {"text": [], "keywords": []}
        for keyword in self.keywords:

            def filterByKeyword(tag):
                return (
                    tag.name != "script"
                    and tag.name != "style"
                    and tag.string
                    and keyword in tag.string
                )

            text = [text.string for text in self.soup.find_all(filterByKeyword)]
            if text:
                textWithKeyword["text"] = textWithKeyword["text"] + [
                    text.string for text in text
                ]
                textWithKeyword["keywords"] = textWithKeyword["keywords"] + [keyword]

        if textWithKeyword["text"]:
            self.textWithKeyWords = self.textWithKeyWords + [
                {"textsWithKeyWords": textWithKeyword, "page": self.url}
            ]

    def getInternalLinks(self):
        internalLinks = []
        for anchor in self.soup.find_all("a"):
            href = anchor.get("href")
            if (
                (not urlparse(href).netloc or self.domain in href)
                and href
                and "www." not in href
            ):
                url = self.getFullUrl(href)
                if url == True:
                    pass
                elif url not in self.internalLinks:
                    internalLinks.append(url)

        self.internalLinks = self.internalLinks + internalLinks

    def getPageData(self, url):
        goturl = self.openUrl(url)
        if goturl:
            self.findTextWithKeyword()
            self.getInternalLinks()
            return goturl

    def iterateThroughInternalLinks(self, recusions=0):
        self.getRunTime()
        if self.timeout:
            print(
                f"timeout",
            )
            return
        else:
            recusions += 1
            print(
                f"thread:{self.idx}   iterateThroughInternalLinks   recursion:{recusions}   links:{len(self.internalLinks)}  runtime:{int(time.time()-self.startTime)}",
            )
            while self.internalLinks and not self.timeout:
                if self.internalLinks[0] not in self.visitedUrls:
                    goturl = self.getPageData(self.internalLinks[0])
                    if goturl:
                        self.iterateThroughInternalLinks(recusions)
                try:
                    self.internalLinks.pop(0)
                except:
                    print("list probably empty")

    def close(self):
        self.driver.quit()
