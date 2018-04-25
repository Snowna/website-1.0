import requests
import json

h = {'Content-type':'application/json','api-key':'+jL8YZ7kPZRgU4oRErWl7du+1jrmZKZA3ME45u41XA0'}

url = 'https://api.shipengine.com/v1/tracking?carrier_code=ups&tracking_number=1ZE2Y229P218333126'
r = requests.get(url, headers = h)
txt = 'F:\\trackTest.txt'
f = open(txt,"w+")
f.write(json.dumps(r.json()))

"""
print(r.json())
"""
