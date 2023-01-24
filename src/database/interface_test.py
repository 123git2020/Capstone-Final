from DBInterface import DBInterface
from dotenv import dotenv_values
env = dotenv_values('.env')

if __name__ == '__main__':
    # PASSWORD can be found from important.txt, eventually use dotenv
    inter = DBInterface("classification_db", "TL63", env['PASSWORD'], 5432)
    # def insert_audio(self, audio_length, path, LAeq, LAmax, LCpeak, TWA):
    inter.insert_audio(2, 'test123', 20, 40, 30, 25)
    print(inter.retrieve_audio_by_path('test123'))
    # inter.remove_by_path("test123")