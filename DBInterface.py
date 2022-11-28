# pip install psycopg2
import psycopg2
class DBInterface:
    def __init__(self, dbname, user, password, port):
        self._conn = psycopg2.connect(dbname=dbname, user=user, password=password, port=port)
        self._conn.set_session(autocommit=True)
        self._cur = self._conn.cursor()
        
    def insert_entry(self, audio_filename, audio_metadata, label):
        try:
            self._cur.execute(f"INSERT INTO audio(audio_filename, audio_metadata, label) VALUES(%s, %s, %s);", (audio_filename, audio_metadata, label))
            self._conn.commit()
        except: 
            print("issue with insert")
            self._conn.rollback()

    def retrieve_by_filename(self, audio_filename):
        self._cur.execute(f"SELECT * FROM audio WHERE (audio_filename=%s);", (audio_filename,))
        return self._cur.fetchone()

    def retrieve_by_metadata(self, audio_metadata):
        self._cur.execute(f"SELECT * FROM audio WHERE (audio_filename=%s);", (audio_metadata,))
        return self._cur.fetchone()

    def retrieve_all_label(self, label):
        self._cur.execute(f"SELECT * FROM audio WHERE (label=%s);", (label,))
        return self._cur.fetchall()
  
    def remove_entry(self, audio_filename):
        self._cur.execute(f"DELETE FROM audio WHERE (audio_filename=%s);", (audio_filename,))
  
# PASSWORD can be found from important.txt, eventually use dotenv
inter = DBInterface("classification_db", "postgres", PASSWORD, 5433)
inter.insert_entry("test_interface1", "test_interface2", "test_interface3")
print(inter.retrieve_by_filename("test_interface1"))
print(inter.retrieve_by_filename("test1"))
inter.remove_entry("test_interface1")