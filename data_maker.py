import requests
import urllib.request
import os
import pandas as pd
import ssl
import re

links = []
data = []
types = ['cigarettes', 'humans']

for type in types:
    for i in range(20):
        params = {
            'page': str(i + 1),
            'per_page': '30',
            'query': type,
        }
        response = requests.get('https://unsplash.com/napi/search/photos', params=params)
        t = response.json()
        for j in t['results']:
            links.append(j['urls']['raw'])
        print(len(links))

current_dir = os.getcwd()
picture_folder = os.path.join(current_dir, "pictures")
if not os.path.exists(picture_folder):
    os.makedirs(picture_folder)
print(picture_folder)

ssl._create_default_https_context = ssl._create_unverified_context

for i in range(len(links)):
    link = links[i]
    type = types[i//600]
    filename = re.sub('[^0-9a-zA-Z]+', '_', type) + str(i + 100 - 600 * (i // 600)) + ".jpg"
    filepath = os.path.join(picture_folder, filename)
    urllib.request.urlretrieve(link, filepath)
    data.append({
        "type": type,
        "picture": filepath
    })


df = pd.DataFrame.from_records(data)
df.to_csv("./cigarette_classification.csv")