# Database Schema: classification_db  
The `audio` table represents each audio file. The `event` table represents the different audio sources present in each audio file and has a many-to-one relationship with the `audio` table. Deleting an entry from the `audio` table will delete the corresponding entry from the `event` table.

### Table: audio

| audio_id | start_time | audio_length | path | LAeq | LAmax | LCpeak | TWA | 
| ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | 
| int | timestamp without timezone ex. `2023-01-08 17:41:16.763289` | numeric | text, relative path | numeric | numeric | numeric | numeric |

### Table: event
| event_id | audio_id | start_time | end_time | path | label |
| ----------- | ----------- | ----------- | ----------- | ----------- | ----------- |
| int | int, foreign key to `audio(audio_id)` | timestamp without timezone ex. `2023-01-08 17:41:16.763289` | timestamp without timezone ex. `2023-01-08 17:41:16.763289` | text, relative path | text |

## PostgreSQL Setup
To create the tables, enter the following SQL statements.
```
CREATE TABLE audio (
    "id" INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    ts TIMESTAMP,
    audio_path TEXT,
    car_horn BOOLEAN DEFAULT FALSE,
    car_passing BOOLEAN DEFAULT FALSE,
    engine BOOLEAN DEFAULT FALSE,
    siren BOOLEAN DEFAULT FALSE,
    speech BOOLEAN DEFAULT FALSE,
    footsteps BOOLEAN DEFAULT FALSE
);
```
Create a table for each of the labels while replacing the name.
```
CREATE TABLE car_passing (
    "id" INT,
    ts TIMESTAMP,
    audio_path TEXT,
    car_passing_label BOOLEAN DEFAULT FALSE
);
```
Create triggers to create or delete rows when rows get inserted or deleted from `audio`.
```
CREATE OR REPLACE FUNCTION insert_child_tables()
    RETURNS TRIGGER
    LANGUAGE PLPGSQL
  AS
$$
BEGIN
    INSERT INTO car_horn(id, ts, car_horn_label, audio_path)
    VALUES(NEW.id, NEW.ts, NEW.car_horn, NEW.audio_path);
    INSERT INTO car_passing(id, ts, car_passing_label, audio_path)
    VALUES(NEW.id, NEW.ts, NEW.car_passing, NEW.audio_path);
    INSERT INTO engine(id, ts, engine_label, audio_path)
    VALUES(NEW.id, NEW.ts, NEW.engine, NEW.audio_path);
    INSERT INTO siren(id, ts, siren_label, audio_path)
    VALUES(NEW.id, NEW.ts, NEW.siren, NEW.audio_path);
    INSERT INTO speech(id, ts, speech_label, audio_path)
    VALUES(NEW.id, NEW.ts, NEW.speech, NEW.audio_path);
    INSERT INTO footsteps(id, ts, footsteps_label, audio_path)
    VALUES(NEW.id, NEW.ts, NEW.footsteps, NEW.audio_path);
	RETURN NEW;
END;
$$

CREATE OR REPLACE FUNCTION delete_child_tables()
    RETURNS TRIGGER
    LANGUAGE PLPGSQL
  AS
$$
BEGIN
    DELETE FROM car_horn WHERE id=OLD.id;
    DELETE FROM car_passing WHERE id=OLD.id;
    DELETE FROM engine WHERE id=OLD.id;
    DELETE FROM siren WHERE id=OLD.id;
    DELETE FROM speech WHERE id=OLD.id;
    DELETE FROM footsteps WHERE id=OLD.id;
	RETURN NEW;
END;
$$

CREATE TRIGGER insert_children
    BEFORE INSERT
    ON audio
    FOR EACH ROW
    EXECUTE PROCEDURE insert_child_tables();

CREATE TRIGGER delete_children
    AFTER DELETE
    ON audio
    FOR EACH ROW
    EXECUTE PROCEDURE delete_child_tables();
```
To create some dummy data, use the following statements to insert and delete.
```
INSERT INTO audio(ts, car_horn, car_passing, engine, siren, speech, footsteps, audio_path)
VALUES (now(), TRUE, FALSE, FALSE, FALSE, FALSE, FALSE, 'test123');

DELETE FROM audio WHERE id=1;
```
