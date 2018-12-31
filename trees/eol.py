import requests
import os
import json
import csv

import imagenet_utils as imnet

from . import data

def get_images(eol_id):
    """Return a generator of urls corresponding to an id."""
    page = 1
    while True:
        details_url = f"https://eol.org/api/pages/1.0/{eol_id}.json"
        payload = {"id": eol_id, 
           "images_per_page": 75,
           "images_page": page,
           }
        r = requests.get(details_url, params=payload)

        response = json.loads(r.text)
        content = response["taxonConcept"]
        if not "dataObjects" in content:
            return

        for item in content["dataObjects"]:
            yield item["mediaURL"]
        page += 1
        
        
def search(query):
    """Return the first id of search query."""
    search_url = "https://eol.org/api/search/1.0.json"
    payload = {"q": query,}
    
    r = requests.get(search_url, params=payload)
    response = json.loads(r.text)
    if len(response["results"]) == 0:
        return

    return response["results"][0]["id"]

def download(query, destination='', max_items=None):
    """Download images associated with query."""
    destination = os.path.join(destination, query)
    eol_id = search(query)
    urls = []
    for idx, url in enumerate(get_images(eol_id)):
        filepath = os.path.join(destination, str(idx))
        data.download_image(url, filepath)
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
            download(tree_name, destination="data/processed")

