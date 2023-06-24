from scripts.fileManager import *
from scripts.functions import *


class scrapedDomainTracker:
    def __init__(self, csv) -> None:
        self.fileManager = fileManager("scrapedDomain.json")
        self.data = self.fileManager.loadData()
        if self.data:
            self.resetInprogress()
        else:
            self.loadInData(csv)
            self.saveData()

    def loadInData(self, file):
        sites = readCsvFile(file)

        for i in sites:
            if i == [" "]:
                sites.remove(i)
        self.data = {
            "Completed": [],
            "Incompleted": sites,
            "Inprogress": [],
        }

    def selectDomain(self):
        if self.data["Incompleted"]:
            self.domain = self.data["Incompleted"].pop(0)
            domainCopy = self.domain[:]

            def onComplete():
                if domainCopy in self.data["Inprogress"]:
                    self.data["Inprogress"].remove(domainCopy)
                    self.data["Completed"].append(domainCopy)
                else:
                    print("dogshitcodegetyourshittogetherman")

            self.data["Inprogress"].append(self.domain)
            return self.domain, onComplete
        else:
            print("scrapedDomainTracker incomplete list empty")

    def resetInprogress(self):
        for i in range(len(self.data["Inprogress"])):
            domain = self.data["Inprogress"].pop(0)
            self.data["Incompleted"].append(domain)

    def saveData(self):
        self.fileManager.updateSelfDotData(self.data)
        self.fileManager.save()
