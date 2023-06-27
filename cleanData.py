
from scripts.functions import *


import sys


max_field_size = 300000000

csv.field_size_limit(max_field_size)



def read_specific_row(csv_file):
    with open(csv_file, "r", encoding="utf-8") as file:
        csv_reader = csv.reader(file)
        file = 0
        for i, row in enumerate(csv_reader):
            if i!=0:
                arr=eval(row[7])
                row=row[:7]+arr
                updateCsv(row, f"data/dump/dump.csv")




read_specific_row("data/someData.csv")
