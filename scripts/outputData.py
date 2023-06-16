from scripts.gpt import *
from scripts.fileManager import *
from scripts.functions import *
import csv


def join(arr):
    newArr = []
    for i in arr:
        newArr = newArr + i["textsWithKeyWords"]["text"]
    return "\n".join(list(set(newArr)))


class outputData:
    def __init__(self, data, domain, domainData, keywords, duplicateText) -> None:
        print("saving output data" + domain)
        self.updateOutputFile([data, domainData])
        self.doaminaData = domainData
        self.keywords = fileManager("keywords.json").loadData()
        self.data = data
        self.string = join(data)[:6000]
        response = chatApiCall(
            self.prompt(),
            1,
        )

        content = response["choices"][0]["message"]["content"]
        boolkeywords, textArr = getBoolKeywordsAndFlattenText(data)
        "/////".join(textArr)
        self.outputcsv = domainData + [content] + ["/////".join(textArr)] + boolkeywords
        self.updateCsv(self.outputcsv)
        for i in duplicateText:
            boolkeywordspage = getBoolKeywordsPage(i["textsWithKeyWords"])
            self.outputcsv = (
                [i["page"]]
                + domainData[1:]
                + ["na"]
                + ["/////".join(i["textsWithKeyWords"]["text"])]
                + boolkeywordspage
            )
            self.updateCsv(self.outputcsv)

    def prompt(self):
        return (
            f"Check the provided text for any statements related to environmental or sustainability issues. Provide a consise summary of those statements, and then list direct quotes from the text in another section to support your summary :{self.string}",
        )[0]

    def updateOutputFile(self, data):
        fileManager("outputFile.json").updateFile(data)

    # def flattenData(self):
    #     return [
    #         [self.inputData[0]["domain"]],
    #         [self.inputData[0]["quotes"]],
    #         [self.inputData[0]["pagesWithKeywords"]["text"][0]],
    #         [self.inputData[0]["pagesWithKeywords"]["text"][1]],
    #         [self.inputData[0]["pagesWithKeywords"]["url"]],
    #     ]

    def updateCsv(self, data):
        with open("data/data.csv", mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(data)

    def firstLineCsv():
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
