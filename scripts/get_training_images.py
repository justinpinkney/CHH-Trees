from pathlib import Path
from tqdm import tqdm

from trees import data

tree_data = data.load_trees()
labels = set([x[3] for x in tree_data])
print(len(labels))
for label in labels:
    print(f"Loading label file for {label}")
    label_file = f'data/train/{label}.txt'
    with open(label_file, 'rt') as f:
        urls = f.readlines()

    success = 0
    total = len(urls)
    print(f"Attempting to download {total} images for {label}")
    label_directory = Path('data', 'train', 'images', label)
    label_directory.mkdir(parents=True, exist_ok=True)
    for idx, url in enumerate(tqdm(urls)):
        filepath = Path(label_directory, f'{idx:06d}')
        result = data.download_image(url, filepath)
        if result:
            success += 1
    print(f"Finished downloading, {success} succeeded.")
        