from DBInterface import DBInterface
from dotenv import dotenv_values
env = dotenv_values('.env')

if __name__ == '__main__':
    # PASSWORD can be found from important.txt, eventually use dotenv
    inter = DBInterface("classification_db", "TL63", env['PASSWORD'], 5432)
    # LAeq, LAmax, LCpeak, TWA
    inter.insert_single_label(2, 'test123', -26.422065767515026, 38.29168175196608, 37.665863985805494, 80.3988680369871, 'siren')
    print(inter.get_audio_by_path('test123'))
    # inter.remove_by_path("test123")
    
    '''
    A1_avg value = -26.422065767515026
A1_max value = 38.29168175196608
C1_peak value = 37.665863985805494
TWA value = 80.3988680369871'''