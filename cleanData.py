if (
    "eco"
    in "I dealt with two staff members trying to switch over my account to our new address and they were both very helpful. The second lady I spoke to (sorry I forgot her name) was excellent & made the whole process very easy!"
):
    print("here")
# from scripts.functions import *

# import pandas as pd
# import sys
# import time

# max_field_size = 300000000

# csv.field_size_limit(max_field_size)


# def validData(row):
#     dataValid = False
#     invalid = False
#     for j, data in enumerate(row):
#         if j > 6:
#             if data == "True":
#                 dataValid = True
#                 print("+valid+")
#             elif not (data == "True" or data == "False"):
#                 invalid = True
#         if j > 46:
#             dataValid = False
#             print("more than 46")
#         total = j
#     if invalid:
#         dataValid = False
#     if total != 46:
#         dataValid = False
#     if (
#         "</id>" in row[6]
#         or "</div>" in row[6]
#         or "</li>" in row[6]
#         or "</title>" in row[6]
#         or 'alt="' in row[6]
#         or "text-align" in row[6]
#         or "display:" in row[6]
#         or '"]' in row[6]
#         or "}" in row[6]
#     ):
#         dataValid = False
#     return dataValid


# def read_specific_row(csv_file):
#     with open(csv_file, "r", encoding="utf-8") as file:
#         csv_reader = csv.reader(file)
#         file = 0
#         for i, row in enumerate(csv_reader):
#             if i % 50000 == 0:
#                 file += 1

#             try:
#                 dataValid = validData(row)
#                 if dataValid:
#                     updateCsv(row, f"data/splitData/rawData({file}).csv")
#             except:
#                 pass


# read_specific_row("data/data.csv")
