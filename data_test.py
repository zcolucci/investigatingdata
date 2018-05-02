import numpy as np
import pandas as pd
from datetime import datetime, timedelta

disaster_file = open("files/earthquake.csv")
pgr_file = open("files/PGR1.csv")
alls_file = open("files/ALL.csv")
aig_file = open("files/Aig1973.csv")
disaster = pd.read_csv(disaster_file)
pgr = pd.read_csv(pgr_file)
alls = pd.read_csv(alls_file)
aig = pd.read_csv(aig_file)

'''
disaster["Tornado"] = float("NaN")
disaster["Tornado"][disaster["Disaster Type"] == "Tornado"] = 1
disaster["Tornado"][disaster["Disaster Type"] != "Tornado"] = 0

print disaster["Tornado"]

tornadoes = []
ids = []
for i in range(len(disaster)):
    if (disaster["Disaster Type"][i] == "Earthquake"):
        if (disaster["Declaration Number"][i] not in ids):
            tornadoes.append(disaster["Start Date"][i])
            ids.append(disaster["Declaration Number"][i])
print tornadoes
'''

magnitudes = []
dates = []
for i in range(len(disaster)):
    magnitudes.append(disaster["mag"][i])
    dates.append(disaster["time"][i][0:10])
    print magnitudes[i], dates[i]

pgr_performance = []
sum1 = 0
num = 0
for i in range(len(pgr)):
    if (pgr["Date"][i] in dates):
        percent = ((pgr["Close"][i] - pgr["Open"][i]) / pgr["Open"][i]) *100
        pgr_performance.append((pgr["Date"][i], percent))
        sum1 += percent
        num+=1

print sum1/num

print pgr_performance

