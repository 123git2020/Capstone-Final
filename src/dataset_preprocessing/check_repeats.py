import pandas as pd

if __name__ == '__main__':
    df = pd.read_csv('data\datasets\processed_datasets\combined_dataset\combined.csv')
    seen = set()
    for x in df['fname']:
        if not x in seen:
            seen.add(x)
        else:
            print(x)