from scripts.fileManager import *
import json
import ast

unwantedCharacters = [" ", "-"]


def prepareString(string):
    for i in unwantedCharacters:
        string = string.replace(i, "")
    return string.lower()


def formatJson(file):
    file = fileManager(file)
    words = file.loadData()
    words = [prepareString(i) for i in words]
    file.updateSelfDotData(words)
    file.save()


def readCsvFile(filename):
    with open(filename, "r", encoding="utf-8-sig") as file:
        csv_reader = csv.reader(file)
        data = []
        for row in csv_reader:
            if row:
                data.append(row)
    return data


def updateCsv(data, file):
    with open(file, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(data)


def removeDuplicateFromTextWithKeyWords(arr):
    arr = sorted(arr, key=lambda x: len(x["textsWithKeyWords"]["text"]))

    def ifInSet(set, arr):
        newArr = []

        for i in arr:
            if i not in set:
                newArr.append(i)
        return newArr

    for i in range(len(arr)):
        for j in range(len(arr)):
            if i != j:
                common = set(arr[i]["textsWithKeyWords"]["text"]).intersection(
                    set(arr[j]["textsWithKeyWords"]["text"])
                )
                if common:
                    arr[i]["textsWithKeyWords"]["text"] = ifInSet(
                        common, arr[i]["textsWithKeyWords"]["text"]
                    )
    for i in arr:
        i["textsWithKeyWords"]["text"] = list(set(i["textsWithKeyWords"]["text"]))
        if not i["textsWithKeyWords"]["text"]:
            arr.remove(i)
    arr = sorted(arr, key=lambda x: len(x["textsWithKeyWords"]["text"]), reverse=True)

    return arr


def getBoolKeywordsAndFlattenText(data):
    textArr = []
    boolkeywords = {}
    keywords = [prepareString(word) for word in fileManager("keywords.json").loadData()]
    for i in keywords:
        boolkeywords[i] = False
    for i in keywords:
        for j in data:
            for k in j["textsWithKeyWords"]["text"]:
                if i in k:
                    boolkeywords[i] = True
    boolkeywords = list(boolkeywords.values())
    return boolkeywords


def getBoolKeywordsPage(data):
    boolkeywords = {}
    keywords = [prepareString(word) for word in fileManager("keywords.json").loadData()]
    for i in keywords:
        boolkeywords[i] = False
    for i in keywords:
        for k in data["text"]:
            if i in k:
                boolkeywords[i] = True
    boolkeywords = list(boolkeywords.values())
    return boolkeywords


def chopchop(string):
    string = string[4:]
    substring = "https://"
    index = string[4:].find(substring)
    string1 = string[4:][index:]
    string2 = string[: index + 4]
    return string1, string2


def get_csv_length(file_path):
    with open(file_path, "r", encoding="utf-8-sig") as file:
        reader = csv.reader(file)
        data = list(reader)
        return len(data)
