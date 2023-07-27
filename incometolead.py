from uszipcode import SearchEngine
import pandas
import matplotlib.pyplot as plt

df = pandas.read_csv("FlintLevels.csv", thousands=',')

df = df.infer_objects()

lead = []
income = []
color = []

sr = SearchEngine()
for index, measurement in df.iterrows():
    try:
        income.append(sr.by_zipcode(measurement["Zip Code"]).median_household_income)
        lead.append(measurement["Lead (ppb)"])
        if measurement["Lead (ppb)"] < 15:
            color.append("green")
        else:
            color.append("red")
    except Exception as e:
        continue

plt.scatter(income, lead, c=color)
plt.title("Lead Concentration in Household Tap Water vs. Household Income", fontsize=13, weight='bold', loc="left")
plt.xlabel("Income (USD)")
plt.ylabel("Lead Concentration (ppb)")

plt.ylim([0,1000])
plt.xlim([20000,60000])

plt.show()
