# fname, car_horn, car_passing, engine, siren, speech
import pandas as pd
import shutil
import os
import re

data = {'fname': [], 'source': [], 'car_horn': [], 'car_passing': [], 'engine': [], 'siren': [], 'speech': []}
    
# Processing UrbanSound8k
regex2 = r'engine_idling|car_horn|siren'
df_us8k = pd.read_csv('data/datasets/original_datasets/urban_sound_8k/UrbanSound8K.csv')
df_us8k.set_index('slice_file_name', inplace=True)
try:
    df_us8k = df_us8k.reset_index()  # make sure indexes pair with number of rows
except:
    print("index already at the beginning")

for index, row in df_us8k.iterrows():
    if re.search(regex2, row['class']) != None:
        data['fname'].append(row['slice_file_name'])
        for label in data:
            if label == 'source':
                data[label].append('urbansound8k')
            elif not label == 'fname':
                data[label].append(0)
        if row['class'] == 'car_horn':
            data['car_horn'].pop()
            data['car_horn'].append(1)
        elif row['class'] == 'engine_idling':
            data['engine'].pop()
            data['engine'].append(1)
        elif row['class'] == 'siren':
            data['siren'].pop()
            data['siren'].append(1)
        shutil.copy(
            f'data/datasets/original_datasets/urban_sound_8k/fold{row["fold"]}/{row["slice_file_name"]}', 
            f'data/datasets/processed_datasets/combined_dataset/data/'
        )

# Processing ESC-50
regex3 = r'siren|car_horn|engine'
df_esc50 = pd.read_csv('data\datasets\original_datasets\ESC-50-master\meta\esc50.csv')
for index, row in df_esc50.iterrows():
    if re.search(regex3, row['category']) != None:
        data['fname'].append(row['filename'])
        for label in data:
            if label == 'source':
                data[label].append('esc-50')
            elif not label == 'fname':
                data[label].append(0)
        if row['category'] == 'car_horn':
            data['car_horn'].pop()
            data['car_horn'].append(1)
        elif row['category'] == 'engine':
            data['engine'].pop()
            data['engine'].append(1)
        elif row['category'] == 'siren':
            data['siren'].pop()
            data['siren'].append(1)
        shutil.copy(
            f'data/datasets/original_datasets/ESC-50-master/audio/{row["filename"]}', 
            f'data/datasets/processed_datasets/combined_dataset/data/'
        )
        
# Processing FSD50k
regex4 = r'engine|Vehicle_horn_and_car_horn_and_honking|siren|car_passing_by'
unwanted_classes = r'drill|power_tool|tools|sawing|boat_and_water_vehicle|train|rail_transport|aircraft'
df_fsd50k = pd.read_csv('data\datasets\original_datasets/fsd50k\dev.csv')
new_df = pd.DataFrame(columns=['fname', 'labels', 'mids', 'split'])
for index, row in df_fsd50k.iterrows():
    if re.search(regex3, row['labels']) != None and re.search(unwanted_classes, row['category']) == None:
        data['fname'].append(row['filename'])
        for label in data:
            if label == 'source':
                data[label].append('fsd50k')
            elif not label == 'fname':
                data[label].append(0)
        if row['labels'] == 'Vehicle_horn_and_car_horn_and_honking':
            data['car_horn'].pop()
            data['car_horn'].append(1)
        elif row['labels'] == 'engine':
            data['engine'].pop()
            data['engine'].append(1)
        elif row['labels'] == 'siren':
            data['siren'].pop()
            data['siren'].append(1)
        elif row['labels'] == 'car_passing_by':
            data['car_passing'].pop()
            data['car_passing'].append(1)
            
        new_row = {'fname': row['fname'], 'labels': row['labels'], 'mids': row['mids'], 'split': row['split']}
        new_df.append(new_row, ignore_index=True)
            
        shutil.copy(
            f'data/datasets/original_datasets/ESC-50-master/audio/{row["filename"]}', 
            f'data/datasets/processed_datasets/combined_dataset/data/'
        )

new_df.to_csv('data/datasets/processed_datasets/combined_dataset/fsd50k_dev.csv')

df_final = pd.DataFrame(data)
df_final.set_index('fname', inplace=True)
df_final.to_csv('data/datasets/processed_datasets/combined_dataset/combined.csv')