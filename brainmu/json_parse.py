import json

"""
Version 1.
"""
d = {}

with open('items.json') as f:
    data = json.load(f)
    for elem in data['properties']:
        d[f'{elem["Value"]}'] = f'{elem["Name"]}'
    for el in data['Calls']:
        for i in el['properties']:
            d[f'{i["Value"]}'] = f'{i["Name"]}'
print(d)

"""
Version 2. More complex one

"""
with open('items.json') as file:
    json_data = json.load(file)
    d2 = {
        json_data["properties"][0]["Value"]: 'alpha',
        json_data["properties"][1]["Value"]: 'balloons',
        json_data["properties"][2]["Value"]: 'plankton',
        json_data["Calls"][0]["properties"][0]["Value"]: 'Ford',
        json_data["Calls"][0]["properties"][1]["Value"]: 'hammer',
        json_data["Calls"][0]["properties"][2]["Value"]: 'basketball',
        json_data["Calls"][0]["properties"][3]["Value"]: 'movies',
        json_data["Calls"][1]["properties"][0]["Value"]: 'house',
        json_data["Calls"][1]["properties"][1]["Value"]: 'pizza',
        json_data["Calls"][1]["properties"][2]["Value"]: 'ica cream',

    }
    print(d2)


desired_dict = {
    "properties[0].Value" : "alpha",
    "properties[1].Value" : "balloons",
    "properties[2].Value" : "plankton",
    "Calls[0].properties[0].Value" : "Ford",
    "Calls[0].properties[1].Value" : "hammer",
    "Calls[0].properties[2].Value" : "basketball",
    "Calls[0].properties[3].Value" : "movies",
    "Calls[1].properties[0].Value" : "house",
    "Calls[1].properties[1].Value" : "pizza",
    "Calls[1].properties[2].Value" : "ice cream",
}

print(desired_dict)