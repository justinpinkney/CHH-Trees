import requests
import json

search_url = "https://eol.org/api/search/1.0.json"
payload = {"q": "Fagus sylvatica",}

r = requests.get(search_url, params=payload)
response = json.loads(r.text)
print(response["results"][0])
id = response["results"][0]["id"]
print(id)

def get_images(id):
    page = 1
    while True:
        details_url = f"https://eol.org/api/pages/1.0/{id}.json"
        payload = {"id": id, 
           "images_per_page": 75,
           "images_page": page,
           }
        r = requests.get(details_url, params=payload)

        response = json.loads(r.text)
        content = response["taxonConcept"]
        if not "dataObjects" in content:
            raise StopIteration

        for item in content["dataObjects"]:
            yield item["mediaURL"]
        page += 1
        print(f"getting page {page}")


urls = []
for url in get_images(id):
    urls.append(url)
print(len(urls))
