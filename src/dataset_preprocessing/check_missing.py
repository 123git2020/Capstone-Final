import os
import pandas as pd

if __name__ == '__main__':
    df = pd.read_csv('data\datasets\processed_datasets\combined_dataset\combined.csv')
    for index, row in df.iterrows():
        if not os.path.exists(f'data\datasets\processed_datasets\combined_dataset\data\{row["fname"]}'):
            print(f'{row["fname"]} is missing.\n')