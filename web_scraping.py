import time
import httpx
import pandas as pd

base_URL = "https://www.reddit.com"
Endpoint = "/r/wallstreetbets"
Category = "/new"

URL = base_URL + Endpoint + Category + ".json"

afterpostid = None

dataset = []

for i in range(5):
    params = {
        "limit" : 100,
        "t" : "month",
        "after" : afterpostid
    }
    response = httpx.get(URL, params = params)
    json_data = response.json()

    dataset.extend([rec['data'] for rec in json_data['data']['children']])

    afterpostid = json_data['data']['after']

    time.sleep(0.5)

df = pd.DataFrame(dataset)
df.to_csv('reddit.csv', index= False)