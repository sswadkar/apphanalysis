import requests
import urllib.parse
import pandas
import json

df = pandas.read_csv("FlintLevels.csv", thousands=',')

df = df.infer_objects()

df = df.loc[(pandas.to_numeric(df["Lead (ppb)"]) >= 15) | (pandas.to_numeric(df["Copper (ppb)"]) >= 1300)]

data = {}
json_data = []

for entry in df.values:
    if len(entry) == 10:
        data[str(entry[6]) + " " + str(entry[7]) + ", FLINT, MI, " + str(entry[9])] = (entry[3], entry[5])

keys = list(data.keys())
for datum in range(len(keys)):
    print(f"{datum}/{len(keys)}")
    address = keys[datum]
    url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(address) + '?format=json'

    response = requests.get(url).json()
    post_json_data = {}
    try:
        post_json_data["lat"] = response[0]["lat"]
        post_json_data["long"] = response[0]["lon"]
        post_json_data["lead_levels"] = data[address][0]
        post_json_data["copper_levels"] = data[address][1]
        json_data.append(post_json_data)
    except Exception as e:
        continue

print(json_data)
with open("data.json", "w") as f:
    json.dump(json_data, f)
