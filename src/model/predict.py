from dotenv import load_dotenv
import os
import sys
from pathlib import Path

# TODO: set PYTHONPATH programmatically with a setup.py, or potentially use site.addsitedir()
sys.path.append(Path(__file__).parent.parent.resolve().__str__() + '/database/')

from DBInterface import DBInterface

def predict(path):
    '''
        Predicts the labels in the given audio file. Puts an entry into the database and returns the array of labels. 
        
        Args:
            file (string): Absolute file path of the file. Must be in .wav format.
            
        Returns:
            predictions: Array of predictions above a certain threshold.
    '''
    
    load_dotenv()
    # TODO: connect model_predict to actual model
    # arr = model_predict(path)
    arr = ["label1", "label2"]
    
    filename = Path(path).name
    # PASSWORD can be found from important.txt, eventually use dotenv
    db = DBInterface("classification_db", "postgres", os.getenv('PASSWORD'), 5433)
    db.insert_entry(filename, ", ".join(arr))
    
    return arr