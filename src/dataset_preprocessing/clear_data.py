import os

if '__name__' == '__main__':
    for filename in os.listdir('data/datasets/processed_datasets/combined_dataset/data'):
        os.remove(f'data/datasets/processed_datasets/combined_dataset/data/{filename}')