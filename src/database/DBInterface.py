# pip install psycopg2
import psycopg2
class DBInterface:
    def __init__(self, dbname, user, password, port):
        self._conn = psycopg2.connect(dbname=dbname, user=user, password=password, port=port)
        self._conn.set_session(autocommit=True)
        self._cur = self._conn.cursor()
        
    def insert_audio(self, audio_length, path, LAeq, LAmax, LCpeak, TWA):
        try:
            self._cur.execute(f'INSERT INTO audio(start_time, audio_length, path, "LAeq", "LAmax", "LCpeak", "TWA") VALUES(now(), %s, %s, %s, %s, %s, %s);', (audio_length, path, LAeq, LAmax, LCpeak, TWA,))
            self._conn.commit()
        except Exception as e: 
            print(f'Audio insert entry error: {e}')
            self._conn.rollback()
            
    def insert_audio_time(self, start_time, audio_length, path, LAeq, LAmax, LCpeak, TWA):
        try:
            self._cur.execute(f'INSERT INTO audio(start_time, audio_length, path, "LAeq", "LAmax", "LCpeak", "TWA") VALUES(%s, %s, %s, %s, %s, %s, %s);', (start_time, audio_length, path, LAeq, LAmax, LCpeak, TWA,))
            self._conn.commit()
        except Exception as e: 
            print(f'Audio insert entry error: {e}')
            self._conn.rollback()
            
    def insert_entry(self, audio_id, start_time, end_time, path, label):
        try:
            self._cur.execute(f"INSERT INTO event(audio_id, start_time, end_time, path, label) VALUES(%s, %s, %s, %s, %s);", (audio_id, start_time, end_time, path, label,))
            self._conn.commit()
        except Exception as e: 
            print(f'Event insert entry error: {e}')
            self._conn.rollback()

    def get_audio_by_path(self, path):
        self._cur.execute(f"SELECT * FROM audio WHERE path=%s;", (path,))
        return self._cur.fetchone()

    def get_all_audio(self):
        self._cur.execute(f"SELECT * FROM audio;")
        return self._cur.fetchall()
  
    def remove_by_path(self, path):
        self._cur.execute(f"DELETE FROM audio WHERE path=%s;", (path,))