from scripts.driver import *
from scripts.functions import *
from scripts.fileManager import *
from scripts.scrapedDomainsTracker import *
import threading


tracker = scrapedDomainTracker()
branchDepth = 15  # how
timeOut = 100  # seconds


def startDriver(
    idx,
    domainCompleted=True,
):  # run this function in the thread
    while tracker.data["Incompleted"]:
        if domainCompleted:
            domain, onComplete = tracker.selectDomain()
            domainCompleted == False
            # try:
            driver(domain, f"thread{idx}", branchDepth, timeOut).scrapeDomain()
            domainCompleted = True
            onComplete()
            tracker.saveData()
            # except:
            print(f"driver:{idx} failed")


# driver(
#     "https://www.watties.co.nz/why-watties/107856300158/3-great-sustainable-choices-from-watties",
#     "test",
#     5,
#     timeOut,
# ).scrapeDomain()


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


runThreads(startDriver, 20)  # main loop
tracker.resetInprogress()
runThreads(startDriver, 5)  # clean up #stuck in progress
tracker.resetInprogress()
startDriver("no threads running")

print("Program completed.")
