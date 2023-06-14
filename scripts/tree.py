from scripts.fileManager import *


# this is kind of cool, it maps out the entire website from the links
class tree:
    def __init__(self, branchSize) -> None:
        self.tree = {}
        self.branchSize = branchSize
        pass

    def addLink(self, link):
        arr = link.split("/")
        tree = self.tree
        for i in arr:
            if i not in tree:
                tree[i] = {}
            if len(tree[i]) > self.branchSize:
                return True
            tree = tree[i]

    def saveTreeJson(self):
        fileManager("tree.json", self.tree).save()
