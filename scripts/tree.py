from scripts.fileManager import *


# this is kind of cool, it maps out the entire website from the links
class tree:
    def __init__(self, branchSize) -> None:
        self.tree = {"visted": True}
        self.branchSize = branchSize
        pass

    def addLink(self, link):
        arr = link.split("/")
        tree = self.tree
        for i in arr:
            if i not in tree:
                tree[i] = {"visted": False}
            if len(tree[i]) > self.branchSize:
                return True
            tree = tree[i]

    def visitLink(self, link):
        print(link, "jere")
        arr = link.split("/")[4:]
        tree = self.tree

        for idx, i in enumerate(arr):
            tree = tree[i]
            if idx == (len(arr) - 1):
                tree["visted"] = True

    def saveTreeJson(self):
        fileManager("tree.json", self.tree).save()
