import json

with open("zone1.json", 'r') as f:
    x = json.load(f)
    
print(x)