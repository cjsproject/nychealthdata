from matplotlib import pyplot as plt
from matplotlib.axes import Axes
import numpy as np
import pandas as pd

data = pd.read_csv(
    'https://raw.githubusercontent.com/nychealth/coronavirus-data/master/boro/boroughs-case-hosp-death.csv')
print(data)

x, d, h = [], [], []

tRemoved = 0
tCases = 0

for row, col in data.iterrows():
    if col['SI_CASE_COUNT'] is 0 or col['SI_DEATH_COUNT'] is 0 or col['SI_HOSPITALIZED_COUNT'] is 0:
        continue
    if len(x) > 1:
        x.append(col['SI_CASE_COUNT'])
        d.append(col['SI_DEATH_COUNT'])
        h.append(col['SI_HOSPITALIZED_COUNT'])
        continue
    x.append(col['SI_CASE_COUNT'])
    d.append(col['SI_DEATH_COUNT'])
    h.append(col['SI_HOSPITALIZED_COUNT'])
    #tRemoved += col['SI_DEATH_COUNT']
    #tCases += col['SI_CASE_COUNT']

rateOfCases = 0
removalRate = 0
for i in range(1, len(x)):
    rateOfCases += x[i] - x[i-1]
    removalRate += d[i] - x[i-1]


r = round(abs(rateOfCases/len(x)-1), 4)#tCases / len(x)
a = 1.2625#round(abs(removalRate/len(d)-1), 4)#tRemoved / len(x)


def N():
    return 1


def p():
    return a / r


def phi():
    return r / a


def rz():
    return r * S0 / a


def diff(f):
    h = 0.0000001
    return (f(t + h) - f(t - h)) / 2 * h


def solve(S, I, R):
    for w in range(1, t):
        S.append(S[w - 1] + (-r * S[w-1] * I[w-1]))
        I.append(I[w - 1] + (r * S[w-1] * I[w-1] - a * I[w-1]))
        R.append(R[w - 1] + (a * I[w-1]))

pop = 1000
S = []
I = []
R = []
t = len(x)
I0 = round(x[0]/pop, 4)
I.append(I0)
S0 = N() - I0
S.append(S0)
R0 = 0
R.append(R0)
solve(S, I, R)

print("S(t): ", S, "I(t): ", I, "R(t): ", R, sep='\n')
print(a , r)
#plt.ylim(ymin=0)

plt.plot(np.arange(0, t), S, 'r')
plt.plot(np.arange(0, t), I, 'g')
plt.plot(np.arange(0, t), R, 'b')

plt.xlabel("day")
plt.ylabel("S(t),I(T),R(t)")
plt.title('Susceptibility, infection and recovery')
#plt.autoscale()
plt.show()
