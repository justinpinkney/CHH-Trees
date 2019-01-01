.DEFAULT_GOAL := keeping_track.csv

train_sources : data/raw venv scripts/get_training_urls.py
	mkdir -p data/train/
	python scripts/get_training_urls.py

data/train/images : train_sources scripts/get_training_images.py
	python scripts/get_training_images.py

data/raw :
	mkdir -p data/raw/
	cp /media/nas/CHH-Trees/trees.csv data/raw/trees.csv
	cp /media/nas/CHH-Trees/labels.csv data/raw/labels.csv
	cp -r /media/nas/CHH-Trees/images/ data/raw

keeping_track.csv : data/raw venv parse_data.py check_photo_times.py
	venv/bin/python parse_data.py

clean :
	rm -rf data/raw
	rm -rf data/processed
	rm -rf data/train
	rm -f keeping_track.csv

venv : venv/bin/activate
venv/bin/activate : requirements.txt
	venv/bin/pip install -Ur requirements.txt
	touch venv/bin/activate

environment : venv
	python3.6 -m venv venv
