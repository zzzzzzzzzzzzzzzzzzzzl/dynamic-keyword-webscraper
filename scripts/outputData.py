from scripts.gpt import *
from scripts.fileManager import *
import csv


def join(arr):
    newArr = []
    for i in arr:
        newArr = newArr + i["textsWithKeyWords"]["text"]
    return "\n".join(list(set(newArr)))


class outputData:
    def __init__(self, data, domain) -> None:
        self.data = data
        self.string = join(data)[:6000]
        response = chatApiCall(
            self.prompt(),
            1,
        )
        content = response["choices"][0]["message"]["content"]
        self.inputData = [
            {
                "domain": domain,
                "quotes": content,
                "pagesWithKeywords": data,
            }
        ]
        print("==========================================")
        print("==========================================")
        print("==========================================")
        print("==========================================")
        print("==========================================")
        print(self.inputData)
        print("==========================================")
        print("==========================================")
        print("==========================================")
        print("==========================================")
        print("==========================================")
        self.updateCsv()

    def prompt(self):
        return (
            f"Check the provided text for any statements related to environmental or sustainability issues. Provide a consise summary of those statements, and then list direct quotes from the text in another section to support your summary :{self.string}",
        )[0]

    def updateOutputFile(self):
        fileManager("outputFile.json").updateFile(self.inputData)

    def flattenData(self):
        print(self.inputData[0]["pagesWithKeywords"])
        return [
            [self.inputData[0]["domain"]],
            [self.inputData[0]["quotes"]],
            [self.inputData[0]["pagesWithKeywords"]["text"][0]],
            [self.inputData[0]["pagesWithKeywords"]["text"][1]],
            [self.inputData[0]["pagesWithKeywords"]["url"]],
        ]

    def updateCsv(self):
        with open("data/data.csv", mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(self.inputData)
