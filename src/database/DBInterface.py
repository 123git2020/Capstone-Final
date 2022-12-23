# pip install psycopg2
import psycopg2
class DBInterface:
    def __init__(self, dbname, user, password, port):
        self._conn = psycopg2.connect(dbname=dbname, user=user, password=password, port=port)
        self._conn.set_session(autocommit=True)
        self._cur = self._conn.cursor()
        
    def insert_entry(self, audio_path, labels):
        try:
            self._cur.execute(f"INSERT INTO audio(audio_path, audio_metadata, labels) VALUES(%s, %s, %s);", (audio_path, labels))
            self._conn.commit()
        except: 
            print("issue with insert")
            self._conn.rollback()

    def retrieve_by_filename(self, audio_path):
        self._cur.execute(f"SELECT * FROM audio WHERE (audio_path=%s);", (audio_path,))
        return self._cur.fetchone()

    def retrieve_all_labels(self, labels):
        self._cur.execute(f"SELECT * FROM audio WHERE (labels=%s);", (labels,))
        return self._cur.fetchall()
  
    def remove_entry(self, audio_path):
        self._cur.execute(f"DELETE FROM audio WHERE (audio_path=%s);", (audio_path,))
