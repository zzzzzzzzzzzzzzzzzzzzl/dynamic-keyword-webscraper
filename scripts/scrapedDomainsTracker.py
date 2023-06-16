from scripts.fileManager import *
from scripts.functions import *


class scrapedDomainTracker:
    def __init__(self) -> None:
        self.fileManager = fileManager("scrapedDomain.json")
        self.data = self.fileManager.loadData()
        if self.data:
            self.resetInprogress()
        else:
            self.loadInData("data/inputData.csv")
            self.saveData()

    def loadInData(self, file):
        sites = [i for i in readCsvFile(file)]
        sites.pop(0)
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
