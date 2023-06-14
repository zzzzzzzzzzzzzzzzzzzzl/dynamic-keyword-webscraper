import json, csv, os


class fileManager:
    def __init__(self, filename, data=None) -> None:
        self.filename = filename
        self.data = data
        self.path = self.setFilePath()
        if not data:
            abc = self.loadData()
            if abc:
                self.data = abc
            else:
                self.save()

    def updateFile(self, arr):
        self.data = self.loadData()
        if self.data:
            self.data = self.data + arr
        else:
            self.data = arr
        self.save()

    def setFilePath(self):
        cwd = os.getcwd()
        file_path = os.path.join(cwd, "data", f"{self.filename}")
        return file_path.replace("//", "/")

    def save(self):
        with open(self.path, "w") as json_file:
            try:
                json.dump(self.data, json_file, indent=4)
                print(self.filename, "saved successfully")
            except:
                print("saving to Json failed err")

    def loadData(self):
        try:
            f = open(self.path)
            print("fileLoaded")
            return json.load(f)
        except:
            print("cannot find file path", self.path)
            return False

    def updateSelfDotData(self, data):
        self.data = data
