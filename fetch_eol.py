import requests
import os
import json
import csv
import imagenet_utils as imnet
from tqdm import tqdm

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

def download_eol(query, destination='', max_items=None):
    search_url = "https://eol.org/api/search/1.0.json"
    payload = {"q": query,}
    destination = os.path.join(destination, query)

    r = requests.get(search_url, params=payload)
    response = json.loads(r.text)
    if len(response["results"]) == 0:
        print("no results")
        return

    print(response["results"][0])
    id = response["results"][0]["id"]
    print(id)

    urls = []
    for idx, url in enumerate(get_images(id)):
        image = imnet.core.Image(f"{idx}", url)
        try:
            imnet.core.save_image(image, destination)
        except (requests.exceptions.RequestException, ValueError):
            print("bad url, TODO use eol url")

        print(idx)
        if max_items and idx >= max_items:
            break

if __name__ == "__main__":
    tree_data = "data/raw/trees.csv"
    with open(tree_data) as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            tree_name = row[2]
            print(tree_name)
            download_eol(tree_name, destination="data/processed")

