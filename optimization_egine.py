import pandas as pd
from gekko import GEKKO

m = GEKKO()
n = 5
budget = int(input('Enter campaign budget:'))

'''
A linear optimization won't be realistic; from a business point of view, we
will have our own constraints.
'''

combined = pd.read_csv('results/combined.csv', index_col=0)
channels = list(sorted(combined.index))
coeffs = combined['Mean'].tolist()

# Assign lower bound and upper bound as business constraints
x1 = m.Var(lb=100, ub=budget)
x2 = m.Var(lb=100, ub=budget)
x3 = m.Var(lb=100, ub=budget)
x4 = m.Var(lb=100, ub=budget)
x5 = m.Var(lb=100, ub=budget)

for i in range(n):
    print(f'Channel {i + 1} should not exceed: ', end='')
    z = int(input())
    m.Equation(globals()['x' + str(i + 1)] <= z)

m.Equation(x1 + x2 + x3 + x4 + x5 <= budget)
m.Maximize(coeffs[0] * x1 + coeffs[1] * x2 + coeffs[2] * x3 + coeffs[3] * x4 +
           coeffs[4] * x5)

m.solve(disp=False)
p1 = x1.value[0]
p2 = x2.value[0]
p3 = x3.value[0]
p4 = x4.value[0]
p5 = x5.value[0]

# Print the budget along with the channel names
print('Budgets:\n')
print(str(channels[0]) + ': ' + str(round(p1, 0)))
print(str(channels[1]) + ': ' + str(round(p2, 0)))
print(str(channels[2]) + ': ' + str(round(p3, 0)))
print(str(channels[3]) + ': ' + str(round(p4, 0)))
print(str(channels[4]) + ': ' + str(round(p5, 0)))
