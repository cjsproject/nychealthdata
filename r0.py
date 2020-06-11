import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

from math import log

"""
data = pd.read_json('https://nyc-health-api.herokuapp.com/case-hosp-death')

print(data)
"""

data = pd.read_json('data.json')

print(data)

x = []
d = []

for row, col in data.iterrows():
    if row == 0: continue
    x.append(col['CASE_COUNT'])
    d.append(col['DEATH_COUNT'])

print(x)

peakIndex = 0
peakVal = max(x)

for i in range(len(x)):
    if x[i] == peakVal:
        peakIndex = i


rArr = []
rSum = 0
n = peakIndex

for i in range(peakIndex):
    if x[i] == 0:continue
    r = pow(x[i+1]/x[i], 1/1) - 1
    rArr.append(r)
    rSum += r

print(rArr)
deaths = 0
totalCases = 0

for i in range(peakIndex):
    deaths += d[i]
    if i <= peakIndex:
        totalCases += x[i]

print("\nAverage daily percentage increase: ", rSum/len(rArr))

r = pow(peakVal/x[0], (1/n)) - 1

print("peak daily cases value:", peakVal, "\nPercentage increase of daily cases necessary for the actual growth: ", r)

"""
#print("Simulated Daily Growth:")
simCases = []
for i in range(peakIndex):
    if i == 0:
        cases = x[i]*(r+1)
    else:
        cases *= r+1
    simCases.append(cases)
    #print("Day ", i+1, "Cases: ", round(cases))
"""
print("Actual Day 36 cases:", x[36] )

domain = np.linspace(0, len(x))

a = pow(deaths, (1/n))-1

b = pow(totalCases, (1/n))-1
rz = (b/a)*x[0]*(b+1)
print(a, '\n', b, "contact rate:", b/a, "Susceptible population: ", x[0]*(b+1), "\ndeaths: ", deaths, "Total Cases:", totalCases, "R0: ", rz )

y = -6352/(36*36)*pow(domain-peakIndex, 2) + peakVal

wave = peakVal*np.sin((1/3)*2*np.pi*domain/len(domain)) + 1

euclideanDist = 0
for i in range(len(y)):
        euclideanDist += pow((y[i] - x[i]), 2)

print(pow(euclideanDist, 1/2))


plt.plot(np.arange(0, len(x)), x, 'r')
#plt.plot(np.arange(0, peakIndex), simCases, 'g')
plt.plot(domain,y)
plt.plot(domain,wave)
plt.xlabel("day")
plt.ylabel("cases")
plt.title('cases per day')
plt.savefig("mygraph.png")
plt.show()
