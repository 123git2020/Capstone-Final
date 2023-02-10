import torch, torchaudio
import pandas as pd

from .BEATs import BEATs, BEATsConfig

class BEATs_eval():
    def __init__(self):
        self.checkpoint = torch.load('src/model/beats/model.pt')

        cfg = BEATsConfig(self.checkpoint['cfg'])
        self.BEATs_model = BEATs(cfg)
        self.BEATs_model.load_state_dict(self.checkpoint['model'])
        self.BEATs_model.eval()
        
        df = pd.read_csv('data\datasets\original_datasets/audioset\class_labels_indices.csv')
        self.label_class = {}
        for idx, row in df.iterrows():
            if not row['mid'] in self.label_class:
                self.label_class[row['mid']] = row['display_name']
        
    def predict(self, fname):
        audio_input_16khz = torchaudio.load(fname)
        padding_mask = torch.zeros(*list(audio_input_16khz[0].size())).bool()

        probs = self.BEATs_model.extract_features(audio_input_16khz[0], padding_mask=padding_mask)[0]

        for i, (top5_label_prob, top5_label_idx) in enumerate(zip(*probs.topk(k=5))):
            top5_label = [self.label_class[self.checkpoint['label_dict'][label_idx.item()]] for label_idx in top5_label_idx]
            print(f'Top 5 predicted labels of the {i}th audio are {top5_label} with probability of {top5_label_prob.tolist()}')
            return (top5_label, top5_label_prob)  
        
    