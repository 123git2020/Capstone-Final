'''
this is just an sample, if you only use audio, 'video_id' and 'image' entries are not necessary.
{
    "data": [
        {
            "video_id": "--4gqARaEJE",
            "wav": "/data/sls/audioset/data/audio/eval/_/_/--4gqARaEJE_0.000.flac",
            "image": "/data/sls/audioset/data/images/eval/_/_/--4gqARaEJE_5.000.jpg",
            "labels": "/m/068hy,/m/07q6cd_,/m/0bt9lr,/m/0jbk"
        },
    ]
}
'''

import json
import os
import pandas as pd
from sklearn.model_selection import train_test_split                
df = pd.read_csv('data\datasets\processed_datasets\combined_dataset\combined.csv')

'''     
index,mid,display_name
0,/m/0912c9,"Car horn"
1,/m/03j1ly,"Siren"
2,/m/02mk9,"Engine"
3,/m/09x0r,"Speech"
4,/t/dd00134,"Car passing by"
'''

audio_files = df['fname'].tolist()
targets = [0] * len(audio_files)

# IMPORTANT: IMPLEMENTATION IS FOR SINGLE LABEL DATA (not sure how ast parses multilabel at the moment)
for index, row in df.iterrows():
    if row['car_horn'] == 1:
        targets[index] = '/m/0912c9'
    elif row['car_passing'] == 1:
        targets[index] = '/t/dd00134'
    elif row['engine'] == 1:
        targets[index] = '/m/02mk9'
    elif row['siren'] == 1:
        targets[index] = '/m/03j1ly'
    elif row['speech'] == 1:
        targets[index] = '/m/09x0r'
    
X_train, X_test, y_train, y_test = train_test_split(audio_files, targets, test_size=0.3, random_state=42, stratify=targets)

train_data = {
    "data": []
}

eval_data = {
    "data": []
}

for idx, value in enumerate(X_train):
    entry = {
        "wav": f'./data/datafiles/audio/{value}',
        "labels": y_train[idx]
    }
    
    train_data['data'].append(entry)
    
for idx, value in enumerate(X_test):
    entry = {
        "wav": f'./data/datafiles/audio/{value}',
        "labels": y_test[idx]
    }
    
    eval_data['data'].append(entry)

with open('./src/dataset_preprocessing/train_data_combined.json', 'w', encoding='utf-8') as f:
    json.dump(train_data, f, ensure_ascii=False, indent=4)
    
with open('./src/dataset_preprocessing/eval_data_combined.json', 'w', encoding='utf-8') as f:
    json.dump(eval_data, f, ensure_ascii=False, indent=4)
    