from DBInterface import DBInterface
from dotenv import dotenv_values
import numpy as np
import datetime
import random
env = dotenv_values('.env')
labels = ['car_horn', 'car_passing', 'engine', 'siren']

if __name__ == '__main__':
    db = DBInterface("classification_db", "TL63", env['PASSWORD'], 5432)
    
    i = 0
    for day in range(1, 31):
        for hour in range(24):
            for minute in range(60):
                for second in range(0, 60, 2):
                    if random.random() < 0.002:
                        date = datetime.datetime(2023, 1, day, hour, minute, second)
                        db.insert_audio_time(date, 2, f'test-{i}', np.random.uniform(low=-25.29, high=-6.03), np.random.uniform(low=30.03, high=43.28), np.random.uniform(low=32.11, high=49.66), np.random.uniform(low=-10, high=10))
                        audio_entry = db.get_audio_by_path(f'test-{i}')
                        audio_id = audio_entry[0]
                        start_time = audio_entry[1]
                        path = audio_entry[3]
                        label = random.choice(labels)
                        hour = start_time.hour
                        end_time = datetime.datetime(2023, 1, day, hour, minute, second+1)
                        db.insert_entry(audio_id, start_time, end_time, f'test-{i}', label)
                        if random.random() < 0.3:
                            start_time = datetime.datetime(2023, 1, day, hour, minute, second+1)
                            new_end_time = datetime.datetime(2023, 1, day, hour, minute, second, 500000)
                            new_labels = labels.copy()
                            new_labels.remove(label)
                            db.insert_entry(audio_id, start_time, new_end_time, f'test-{i}-1', random.choice(new_labels))
                            
                        i += 1