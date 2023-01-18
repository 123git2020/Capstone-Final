# fname, car_horn, car_passing, engine, siren, speech, footsteps
import pandas as pd
import shutil
import os
import re

data = {'fname': [], 'car_horn': [], 'car_passing': [], 'engine': [], 'siren': [], 'speech': [], 'footsteps': []}

# Processing isolated urban sound database
df = pd.read_csv('data/datasets/processed_datasets/processed_isolated_urban_sound_database/ProcessedIsolatedUrban.csv')
regex = r"carHorn|cityCar|cityStep|roadCar|stepCity|stopCar|stepPark|voice"

for filename in os.listdir('original_datasets/isolated_urban_sound_database/background/'):
    if re.search(regex, filename) != None:
        shutil.copy(
            f'data/datasets/original_datasets/isolated_urban_sound_database/background/{filename}',
            f'data/datasets/processed_datasets/combined_dataset/data/'
        )
        
for filename in os.listdir('data/datasets/original_datasets/isolated_urban_sound_database/event/'):
    if re.search(regex, filename) != None:
        shutil.copy(
            f'data/datasets/original_datasets/isolated_urban_sound_database/event/{filename}',
            f'data/datasets/processed_datasets/combined_dataset/data/'
        )
        
for filename in os.listdir('data/datasets/processed_datasets/combined_dataset/data/'):
    data['fname'].append(filename)
    for label in data:
        if not label == 'fname':
            data[label].append(0)
            
    match = re.findall(regex, filename)[0]
    if match == 'carHorn':
        data['car_horn'].pop()
        data['car_horn'].append(1)
    elif match == 'cityCar' or match == 'roadCar':
        data['car_passing'].pop()
        data['car_passing'].append(1)
    elif match == 'stopCar':
        data['engine'].pop()
        data['engine'].append(1)
    elif match == 'voice':
        data['speech'].pop()
        data['speech'].append(1)
    elif match == 'stepCity' or match == 'stepPark' or match == 'cityStep':
        data['footsteps'].pop()
        data['footsteps'].append(1)
        
# Processing SONYC
df = pd.read_csv('data/datasets/original_datasets/SONYC/annotations.csv')
df_sonyc = pd.DataFrame({'fname': []}).set_index('fname')
df_sonyc['fname'] = df['audio_filename']
df_sonyc['car_horn'] = [int(x) for x in df['5-1_car-horn_presence']]
df_sonyc['car_passing'] = [0] * len(df['audio_filename'])
df_sonyc['engine'] = [int(x) for x in df['1_engine_presence']]
df_sonyc['siren'] = [int(x) for x in df['5-3_siren_presence']]
df_sonyc['speech'] = [int(x) for x in df['7_human-voice_presence']]
df_sonyc['footsteps'] = [0] * len(df['audio_filename'])
df_sonyc.drop_duplicates(subset="fname", keep='first', inplace=True)
df_sonyc.drop(df_sonyc[df_sonyc['engine'] + df_sonyc['car_horn'] + df_sonyc['siren'] + df_sonyc['speech'] == 0].index, inplace=True)

try:
    df_sonyc = df_sonyc.reset_index()  # make sure indexes pair with number of rows
except:
    print("index already at the beginning")

for index, row in df_sonyc.iterrows():
    shutil.copy(
        f'data/datasets/original_datasets/SONYC/data/{row["fname"]}', 
        f'data/datasets/processed_datasets/combined_dataset/data/'
    )
    
# Processing UrbanSound8k
regex2 = r'engine_idling|car_horn|siren'
df_us8k = pd.read_csv('data/datasets/original_datasets/urban_sound_8k/UrbanSound8K.csv')
df_us8k.rename({'slice_file_name': 'fname'}, inplace=True)
df_us8k.set_index('slice_file_name', inplace=True)
df_us8k.drop(columns=['start', 'end', 'salience', 'fsID', 'classID'], inplace=True)
try:
    df_us8k = df_us8k.reset_index()  # make sure indexes pair with number of rows
except:
    print("index already at the beginning")

for index, row in df_us8k.iterrows():
    if re.search(regex2, row['class']) != None:
        data['fname'].append(row['slice_file_name'])
        for label in data:
            if not label == 'fname':
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
            f'data/datasets/processed_datasets/processed_urban_sound_8k/data/'
        )
        
df_us8k.drop(columns=['class', 'fold'], inplace=True)
    
df_final = pd.DataFrame(data)
result = pd.concat([df_final, df_sonyc])
result.to_csv('data/datasets/processed_datasets/combined_dataset/combined.csv')