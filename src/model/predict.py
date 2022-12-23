from database.DBInterface import DBInterface
from pathlib import Path

def predict(path):
    '''
        Predicts the labels in the given audio file. Puts an entry into the database and returns the array of labels. 
        
        Args:
            file (string): Absolute file path of the file. Must be in .wav format.
            
        Returns:
            predictions: Array of predictions above a certain threshold.
    '''
    
    # TODO: connect model_predict to actual model
    arr = model_predict(path)
    
    filename = Path(path).name
    # PASSWORD can be found from important.txt, eventually use dotenv
    db = DBInterface("classification_db", "postgres", PASSWORD, 5433)
    db.insert_entry(filename, ", ".join(arr))
    
    return arr
    
    
    