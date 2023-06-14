from scripts.fileManager import *

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
                print(row[0])
                data.append(row[0])
    return data


def removeDuplicateFromTextWithKeyWords(arr):
    arr = sorted(arr, key=lambda x: len(x["textsWithKeyWords"]["text"]))
    for i in arr:
        print(i)

    def ifInSet(set, arr):
        newArr = []

        for i in arr:
            if i not in set:
                newArr.append(i)
        return newArr

    for i in range(len(arr)):
        for j in range(len(arr)):
            if i != j:
                print(arr[i])
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
