import json
import glob

import pandas as pd

import check_photo_times as util

labels = "data/raw/labels.json"
trees = "data/raw/trees.csv"
images = "data/raw/images"

with open(labels) as label_file:
    label_data = json.loads(label_file.read())

label_list = []
for item in label_data:
    label_list.append({'filename': item['External ID'],
                        'tree_id': item['Label']['tree_id'],
                        })

label_df = pd.DataFrame(label_list).set_index("filename")


taken_data = util.get_all_creation_times(images)
taken_df = pd.DataFrame(taken_data).set_index("filename")

db = label_df.join(taken_df)
db['month'] = [x.month for x in db['taken_at']]
db = db.groupby(['tree_id', 'month']).count()
db = db.unstack()
print(db)
db.to_csv('keeping_track.csv')
#print(db.set_index('taken_at').resample('M'))
#print(db["tree_id"].value_counts())
