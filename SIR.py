from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

data = pd.read_csv(
    'https://raw.githubusercontent.com/nychealth/coronavirus-data/master/boro/boroughs-case-hosp-death.csv')

x, d, h = [], [], []

tRemoved = 0
tCases = 0
for row, col in data.iterrows():
    x.append(col['SI_CASE_COUNT'])
    d.append(col['SI_DEATH_COUNT'])
    h.append(col['SI_HOSPITALIZED_COUNT'])
    tRemoved += d[-1]
    tCases += x[-1] + h[-1]

# get the index (day) of first index of the first case,
# x.index(1), start t at that length,
# truncate x to that point

h = h[x.index(1):-1]
d = d[x.index(1):-1]
x = x[x.index(1):-1]

print(x, d, h, sep='\n')

rateOfCases = 0
removalRate = 0
for i in range(1, len(x)):
    rateOfCases += x[i] - x[i - 1]
    removalRate += d[i] - x[i - 1]


def N():
    return 1


def p():
    return a / r


def phi():
    return r / a


def rz():
    return [(z * S0 / y) for z in r for y in a]


def solve():
    for w in range(1, t):
        if w < 30:
            S.append(round(S[w - 1] + (-r[0] * S[w - 1] * I[w - 1]), 4))
            I.append(round(I[w - 1] + (r[0] * S[w - 1] * I[w - 1] - a[0] * I[w - 1]), 4))
            R.append(round(R[w - 1] + (a[0] * I[w - 1]), 4))
        else:
            S.append(round(S[w - 1] + (-r[1] * S[w - 1] * I[w - 1]), 4))
            I.append(round(I[w - 1] + (r[1] * S[w - 1] * I[w - 1] - a[1] * I[w - 1]), 4))
            R.append(round(R[w - 1] + (a[1] * I[w - 1]), 4))


pop = 1000  #some population, generally small
r = []  # change in cases for the first 14 days, compared to the total population
a = []  # change in deaths over the first 14 days, compared to the total population
r.append(abs((x[x.index(730)]-x[0])/pop))
r.append(abs((x[-1]-x[x.index(730)])/pop))
a.append(abs((d[x.index(730)]-d[0])/pop))
a.append(abs((d[-1]-d[x.index(730)])/pop))
S = []
I = []
R = []
t = len(x)
I0 = round(x[0] / pop, 4)
I.append(I0)
S0 = N() - I0
S.append(S0)
R0 = 0
R.append(R0)
solve()

print("S(t): ", S, "I(t): ", I, "R(t): ", R, sep='\n')
print(r, a, rz(), sep='\n')

plt.plot(np.arange(0, t), S, 'r')
plt.plot(np.arange(0, t), I, 'g')
plt.plot(np.arange(0, t), R, 'b')

plt.xlabel("Time (Days)\nBasic Reproduction: "+str(rz()))
plt.ylabel("S(t), I(T), R(t)")
plt.title('Susceptibility (r), Infection (g) and Recovery (b)')
plt.show()
