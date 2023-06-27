from scripts.gpt import *
from scripts.fileManager import *
from scripts.functions import *
import csv


class outputData:
    def __init__(self, data, domain, textWithKeyWords, keywords) -> None:
        print("saving output")
        self.data = data
        self.doamina = domain
        self.keywords = keywords
        self.textWithKeyWords = textWithKeyWords
        self.data = data
        self.domainInput()
        self.pageInput()

    def domainInput(self):
        text, keywords = getDomainKeywords(self.textWithKeyWords)
        self.string = text[:6000]
        response = chatApiCall(
            self.prompt(),
            1,
        )

        content = response["choices"][0]["message"]["content"]
        inputData = self.data + [content] + [text] + [keywords]
        self.updateCsv(inputData)

    def pageInput(self):
        for i in self.textWithKeyWords:
            text, keywords, page = getpageKeywords(i)
            inputData = [page] + self.data[1:] + ["na"] + [text] + keywords
            self.updateCsv(inputData)

    def prompt(self):
        return (
            f"Check the provided text for any statements related to environmental or sustainability issues. Provide a consise summary of those statements, and then list direct quotes from the text in another section to support your summary :{self.string}",
        )[0]

    def updateOutputFile(self, data):
        fileManager("outputFile.json").updateFile(data)

    def updateCsv(self, data):
        with open("data/data.csv", mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(data)

    def firstLineCsv(self):
        line = [
            "www",
            "ANZSIC06_2Digit",
            "Subdivision descriptor",
            "ANZSIC06",
            "Description",
            "Summary of claims	",
            "Text containing keywords",
        ] + fileManager("keywords.json").loadData()
        with open("data/data.csv", mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(line)
