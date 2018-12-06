.DEFAULT_GOAL := keeping_track.csv

data/raw :
	mkdir -p data/raw/
	cp /media/nas/CHH-Trees/trees.csv data/raw/trees.csv
	cp /media/nas/CHH-Trees/labels.json data/raw/labels.json
	cp -r /media/nas/CHH-Trees/images/ data/raw

keeping_track.csv : data/raw venv parse_data.py
	venv/bin/python parse_data.py

clean :
	rm -rf data/raw

venv : venv/bin/activate
venv/bin/activate : requirements.txt
	venv/bin/pip install -Ur requirements.txt
	touch venv/bin/activate

environment : venv
	python3.6 -m venv venv
