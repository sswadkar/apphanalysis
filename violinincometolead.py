from uszipcode import SearchEngine
import pandas
import matplotlib.pyplot as plt
import numpy as np

df = pandas.read_csv("FlintLevels.csv", thousands=',')

df = df.infer_objects()

def closestTo(income, income_categories):
    income_range = 0
    distance = 100000000
    for cat in income_categories:
        if abs(income-cat) < distance:
            income_range = cat
            distance = abs(income-cat)

    return income_range

income_categories = []
min_income = 20_000
max_income = 60_000

for income_range in range(min_income, max_income, 5000):
    income_categories.append(income_range)
income_categories.append(max_income)

lead = {}
income = []
color = []

sr = SearchEngine()
for index, measurement in df.iterrows():
    try:
        output = closestTo(sr.by_zipcode(measurement["Zip Code"]).median_household_income, income_categories)
        income.append(output)
        if output not in list(lead.keys()):
            lead[output] = []
        if (measurement["Lead (ppb)"]) < 1000:
            lead[output].append(measurement["Lead (ppb)"])
        if measurement["Lead (ppb)"] < 15:
            color.append("green")
        else:
            color.append("red")
    except Exception as e:
        continue

lead = dict(sorted(lead.items()))

plt.violinplot(list(lead.values()), showmedians=True)
plt.xticks(np.arange(1, 10), [str(cat) for cat in list(lead.keys())])
# plt.violinplot(list(lead.values()), list(lead.keys()))


plt.title("Lead Concentration in Household Tap Water vs. Household Income", fontsize=13, weight='bold', loc="left")
plt.xlabel("Income (USD)")
plt.ylabel("Lead Concentration (ppb)")

# plt.ylim([0,1000])
# plt.xlim([20000,60000])

plt.show()
