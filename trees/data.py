import csv
import re
from pathlib import Path
import traceback

import requests
import imagenet_utils as imnet

from trees import eol

LABEL_FILE = "data/raw/trees.csv"

def extract_search_terms(name):
    qual_removed = re.sub(r'\(.*?\)', '', name)
    search_terms = qual_removed.strip().lower().split('/')
    return tuple(search_terms)

def make_search_list(data):
    """Extract search terms from tree data."""
    terms = dict()
    for item in data:
        tree_id, common_name, scientific_name, label = item
        extracted = extract_search_terms(scientific_name)
        terms[label] = extracted
            
    return terms

def load_trees():
    """Load mapping of ids to species.
    
    Tree data is in the format:
        id, common name, scientific/other names, label
    """
    data = []
    with open(LABEL_FILE) as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            labels = extract_search_terms(row[2])
            row.append(labels[0].replace(' ', '_'))
            data.append(row)
            
    return data

def download_image(url, filepath):
    """Attempts to download an internet image."""
    filepath = Path(filepath)
    image = imnet.core.Image(filepath.name, url)
    try:
        imnet.core.save_image(image, filepath.parent)
        return True
    except (requests.exceptions.RequestException, ValueError):
        print(traceback.format_exc())
        return False

    
def get_imagenet_urls(terms):
    """Get all imagenet urls for a list of search terms."""
    urls = []
    for term in terms:
        results = imnet.search(term)
        if results:
            wnids = [x.wnid for x in results]
            for wnid in wnids:
                urls.extend([x.url for x in imnet.urls(wnid)])
    return urls

def get_eol_urls(terms):
    """Get all eol (original) urls for a list of search terms."""
    urls = []
    for term in terms:
        result = eol.search(term)
        if result:
            eol_images = eol.get_images(result)
            urls.extend(list(eol_images))            
    return urls
