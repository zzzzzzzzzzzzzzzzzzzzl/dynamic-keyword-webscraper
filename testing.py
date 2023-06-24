from scripts.functions import *
from scripts.gpt import *

updateCsv("test this is a test", "data/testfile.csv")

r = chatApiCall("hello test")
print(r)
