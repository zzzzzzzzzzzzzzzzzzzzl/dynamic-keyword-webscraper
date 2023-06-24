from scripts.driver import *
from scripts.functions import *
from scripts.fileManager import *
from scripts.scrapedDomainsTracker import *
import threading

inputCsv = "data/inputData.csv"
tracker = scrapedDomainTracker(inputCsv)
branchDepth = 50  # how
timeOut = 1500  # seconds

csvData = readCsvFile(inputCsv).pop(0)

if get_csv_length("data/data.csv") == 0:
    outputData.firstLineCsv()


def startDriver(
    idx,
    domainCompleted=True,
):
    while tracker.data["Incompleted"]:
        if domainCompleted:
            domain, onComplete = tracker.selectDomain()
            domainCompleted == False
            goodResponse, protocal = statusCode(domain[0])
            try:
                if goodResponse:
                    driver(
                        domain, protocal, f"thread{idx}", branchDepth, timeOut
                    ).scrapeDomain()
                    domainCompleted = True
                    onComplete()
                    tracker.saveData()

                else:
                    updateCsv(domain, "data/badResponse.csv")
                    domainCompleted = True
                    onComplete()
                    tracker.saveData()

            except:
                print(
                    "=========================webdriver failed========================="
                )
                print(
                    "=========================webdriver failed========================="
                )
                print(
                    "=========================webdriver failed========================="
                )
                print(
                    "=========================webdriver failed========================="
                )
                print(
                    "=========================webdriver failed========================="
                )
                print(
                    "=========================webdriver failed========================="
                )
                print(
                    "=========================webdriver failed========================="
                )


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


runThreads(startDriver, 150)  # main loop
# tracker.resetInprogress()
# runThreads(startDriver, 10)  # clean up #stuck in progress
# tracker.resetInprogress()
# runThreads(startDriver, 10)  # clean up #stuck in progress
# tracker.resetInprogress()
# runThreads(startDriver, 10)  # clean up #stuck in progress
# tracker.resetInprogress()
# runThreads(startDriver, 3)  # clean up #stuck in progress
# startDriver("no threads running")

print("Program completed.")
