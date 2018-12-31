from trees import data

from pathlib import Path

if __name__ == "__main__":
    
    print("building label lists for tree data")
    tree_data = data.load_trees()
    search_list = data.make_search_list(tree_data)
    
    for label, terms in search_list.items():    
        filepath = Path('data/train', label + '.txt')
        print(f"writing to {filepath}")
        with open(filepath, 'wt') as url_file:
            url_file.writelines([f"{url}\n" for url in data.get_imagenet_urls(terms)])
            url_file.writelines([f"{url}\n" for url in data.get_eol_urls(terms)])
        print(f"done {label}")
