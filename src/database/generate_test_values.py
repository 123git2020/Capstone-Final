from DBInterface import DBInterface
from dotenv import dotenv_values
import numpy as np
import datetime
import random
env = dotenv_values('.env')

if __name__ == '__main__':
    db = DBInterface("classification_db", "TL63", env['PASSWORD'], 5432)
    for day in range(1, 31):
        for i in range(1, 4):
            date = datetime.datetime(2023, 1, day, 3*i)
            db.insert_audio_time(date, 2, f'test{day}-{i}', np.random.uniform(low=-25.29, high=-6.03), np.random.uniform(low=30.03, high=43.28), np.random.uniform(low=32.11, high=49.66), np.random.uniform(low=-10, high=10))
            audio_entry = db.get_audio_by_path(f'test{day}-{i}')
            audio_id = audio_entry[0]
            start_time = audio_entry[1]
            path = audio_entry[3]
            label = random.choice(['car_horn', 'car_passing', 'engine', 'siren'])
            end_time = datetime.datetime(2023, 1, day, start_time.hour, 0, 1)
            db.insert_entry(audio_id, start_time, end_time, f'test{day}-{i}', label)