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
