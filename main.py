from scripts.driver import *
from scripts.functions import *
from scripts.fileManager import *
from scripts.scrapedDomainsTracker import *
import threading


tracker = scrapedDomainTracker()
branchDepth = 100  # how
timeOut = 1000  # seconds

csvData = readCsvFile("data/inputData.csv").pop(0)
# driver(["https://greypower.co.nz/"], "n", 1, 20)
if get_csv_length("data/data.csv") == 0:
    outputData.firstLineCsv()


def startDriver(
    idx,
    domainCompleted=True,
):  # run this function in the thread
    while tracker.data["Incompleted"]:
        if domainCompleted:
            domain, onComplete = tracker.selectDomain()
            domainCompleted == False
        try:
            driver(domain, f"thread{idx}", branchDepth, timeOut).scrapeDomain()
            domainCompleted = True
            onComplete()
            tracker.saveData()
        except:
            print("=========================webdriver failed=========================")
            print("=========================webdriver failed=========================")
            print("=========================webdriver failed=========================")
            print("=========================webdriver failed=========================")
            print("=========================webdriver failed=========================")
            print("=========================webdriver failed=========================")
            print("=========================webdriver failed=========================")


def runThreads(target, threadCount):
    threadArr = []
    if len(tracker.data["Incompleted"]) < threadCount:
        threadCount = len(tracker.data["Incompleted"])
    for i in range(threadCount):
        threadArr.append(threading.Thread(target=target, args=(i,)))

    for i in threadArr:
        i.start()
    for i in threadArr:
        i.join()


runThreads(startDriver, 10)  # main loop
tracker.resetInprogress()
runThreads(startDriver, 10)  # clean up #stuck in progress
tracker.resetInprogress()
runThreads(startDriver, 10)  # clean up #stuck in progress
tracker.resetInprogress()
runThreads(startDriver, 10)  # clean up #stuck in progress
tracker.resetInprogress()
runThreads(startDriver, 3)  # clean up #stuck in progress
startDriver("no threads running")

print("Program completed.")
