import numpy as np
import pandas as pd
from datetime import datetime, timedelta

disaster_file = open("files/disaster_data.csv")
dow_file = open("files/DowJones1985.csv")
nasdaq_file = open("files/Nasdaq1971.csv")
sandp_file = open("files/SandP1950.csv")
disaster = pd.read_csv(disaster_file)
dow = pd.read_csv(dow_file)
nasdaq = pd.read_csv(nasdaq_file)
sandp = pd.read_csv(sandp_file)

'''
disaster["Tornado"] = float("NaN")
disaster["Tornado"][disaster["Disaster Type"] == "Tornado"] = 1
disaster["Tornado"][disaster["Disaster Type"] != "Tornado"] = 0

print disaster["Tornado"]
'''
tornadoes = []
ids = []
for i in range(len(disaster)):
    if (disaster["Disaster Type"][i] == "Earthquake"):
        if (disaster["Declaration Number"][i] not in ids):
            tornadoes.append(disaster["Start Date"][i])
            ids.append(disaster["Declaration Number"][i])
print tornadoes

dow_performance = []
sum1 = 0
num = 0
for i in range(len(dow)):
    percent = ((dow["Close"][i] - dow["Open"][i]) / dow["Open"][i]) *100
    if (dow["Date"][i] in tornadoes):
        dow_performance.append((dow["Date"][i], percent))
        sum1 += percent
        num+=1

print sum1/num

print dow_performance

