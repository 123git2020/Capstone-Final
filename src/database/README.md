# Database Schema: classification_db  
The table `audio` contains the id, timestamp, labels, and the audio path of each data entry.  All inserts and deletes should be done on the parent table `audio`. Changes to the parent table will be reflected in each of the child tables through triggers. There is a child table for each label ex. `car_horn` containing the id, timestamp, label, and audio path of the entry. 

Note: The id is generated on insert. Do not choose an id value when inserting into `audio`.  

### Table: audio

| id | ts | car_horn | car_passing | engine | siren | speech | footsteps | audio_path | 
| ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | 
| int | timestamp without timezone ex. `2023-01-08 17:41:16.763289` | boolean | boolean | boolean | boolean | boolean | boolean | text, absolute path of file |

### Table: car_horn
| id | ts | car_horn_label | audio_path | 
| ----------- | ----------- | ----------- | ----------- |
| int | timestamp without timezone ex. `2023-01-08 17:41:16.763289` | boolean | text, absolute path of file |

### Table: car_passing
| id | ts | car_passing_label | audio_path | 
| ----------- | ----------- | ----------- | ----------- |
| int | timestamp without timezone ex. `2023-01-08 17:41:16.763289` | boolean | text, absolute path of file |

### Table: engine
| id | ts | engine_label | audio_path | 
| ----------- | ----------- | ----------- | ----------- |
| int | timestamp without timezone ex. `2023-01-08 17:41:16.763289` | boolean | text, absolute path of file |

### Table: footsteps
| id | ts | footsteps_label | audio_path | 
| ----------- | ----------- | ----------- | ----------- |
| int | timestamp without timezone ex. `2023-01-08 17:41:16.763289` | boolean | text, absolute path of file |

### Table: siren
| id | ts | siren_label | audio_path | 
| ----------- | ----------- | ----------- | ----------- |
| int | timestamp without timezone ex. `2023-01-08 17:41:16.763289` | boolean | text, absolute path of file |

### Table: speech
| id | ts | speech_label | audio_path | 
| ----------- | ----------- | ----------- | ----------- |
| int | timestamp without timezone ex. `2023-01-08 17:41:16.763289` | boolean | text, absolute path of file |

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
