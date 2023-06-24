from scripts.fileManager import *
import json
import ast
import requests


unwantedCharacters = [" ", "-"]
badResponse = [400, 401, 403, 404, 500, 503]


def test():
    r = requests.get("http://waihekenativeplants.que.tm")
    print(r.status_code)


def updateCsv(data, file):
    with open(file, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(data)


def statusCode(url):
    http = "http://" + url
    https = "https://" + url
    protocal = None

    try:
        response = requests.get(https)

        if response.status_code in badResponse:
            value = False
        protocal = "https://"
        value = True
    except:
        try:
            response = requests.get(http)

            if response.status_code in badResponse:
                value = False
            protocal = "http://"
            value = True
        except:
            value = False
    return value, protocal


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


def getDomainKeywords(arr):  # input text with keywords arr
    newArr = []
    keyWordDict = arr[0]["keywords"]
    for i in arr:
        for j in i["textsWithKeyWords"]:
            newArr.append(j["text"])
        for j in i["keywords"]:
            if i["keywords"][j]:
                keyWordDict[j] = True
    keywords = [keyWordDict[i] for i in keyWordDict]

    return newArr, keywords


def getpageKeywords(arr):
    newArr = []

    for j in arr["textsWithKeyWords"]:
        newArr.append(j["text"])
    keywords = [arr["keywords"][i] for i in arr["keywords"]]

    return newArr, keywords, arr["page"]
