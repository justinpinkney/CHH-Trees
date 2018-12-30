import csv
import re
import imagenet_utils as imnet

tree_data = "data/raw/trees.csv"

def extract_search_terms(name):
    qual_removed = re.sub(r'\(.*?\)', '', name)
    search_terms = qual_removed.strip().lower().split('/')
    return tuple(search_terms)

def make_search_list(data):
    terms = set()
    for item in data:
        tree_id, common_name, scientific_name = item
        extracted = extract_search_terms(scientific_name)
        label = extracted[0]
        terms.add(extracted)
            
    return terms

def load_trees():
    """Load mapping of ids to species"""
    data = []
    with open(tree_data) as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            data.append(row)
            
    return data
