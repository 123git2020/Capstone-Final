# Database Schema: classification_db  
The `audio` table represents each audio file. The `event` table represents the different audio sources present in each audio file and has a many-to-one relationship with the `audio` table. Deleting an entry from the `audio` table will delete the corresponding entry from the `event` table, so only remove from the `audio` table. `audio_id` in the `audio` table is generated, so do not insert a value for `audio_id` when inserting into the `audio` table.

### Table: audio

| audio_id | start_time | audio_length | path | LAeq | LAmax | LCpeak | TWA | 
| ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | 
| int | timestamp without timezone ex. `2023-01-08 17:41:16.763289` | numeric | text, relative path | numeric | numeric | numeric | numeric |

### Table: event
| event_id | audio_id | start_time | end_time | path | label |
| ----------- | ----------- | ----------- | ----------- | ----------- | ----------- |
| int | int, foreign key to `audio(audio_id)` | timestamp without timezone ex. `2023-01-08 17:41:16.763289` | timestamp without timezone ex. `2023-01-08 17:41:16.763289` | text, relative path | text |

## PostgreSQL Setup
To create the tables, enter the following SQL statements.
```
CREATE TABLE audio (
    audio_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    start_time TIMESTAMP,
    audio_length NUMERIC,
    path TEXT,
    "LAeq" NUMERIC,
    "LAmax" NUMERIC,
    "LCpeak" NUMERIC,
    "TWA" NUMERIC
);

CREATE TABLE event (
    event_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    audio_id INT REFERENCES audio(audio_id) ON DELETE CASCADE,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    path TEXT,
    class TEXT
);
```
To create some dummy data, use the following statements to insert and delete.
```
INSERT INTO audio(start_time, audio_length, path, "LAeq", "LAmax", "LCpeak", "TWA")
VALUES (now(), TRUE, FALSE, FALSE, FALSE, FALSE, FALSE, 'test123');

INSERT INTO event(audio_id, start_time, end_time, path, label)
VALUES({val_from_audio}, now(), now()+1, test123, car_horn);"

DELETE FROM audio WHERE id=1;
```
