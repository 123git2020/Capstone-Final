
#%%
#import wandb
import numpy as np
import os
from tqdm import tqdm
import torch
from torch.utils.data import DataLoader, random_split
import argparse
from sklearn import metrics
import torch.nn.functional as F
import pandas as pd

#from datasets.esc50 import get_test_set, get_training_set
from models.MobileNetV3 import get_model as get_mobilenet
from models.preprocess import AugmentMelSTFT
from helpers.init import worker_init_fn
from helpers.utils import NAME_TO_WIDTH, exp_warmup_linear_down, mixup
from loader import SoundDataset
from prep import ProcessedDataset

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
#%%

#updir=r'C:\WPy64-31090\notebooks\Sound Processing'
metadata=pd.read_csv((r'urban_sound_8k\ProcessedUrbanSound8k.csv'))
#display(metadata)

sound_data = SoundDataset(metadata, r'urban_sound_8k\data/')

proce=ProcessedDataset(sound_data, None)

print(proce[0][0].dtype)
train_set, test_set=random_split(proce,[round(len(sound_data)*0.8),round(len(sound_data)*0.2)])


#%%
def train(args):
    # Train Models for Acoustic Scene Classification

    # logging is done using wandb
    # wandb.init(
    #     project="ESC50",
    #     notes="Fine-tune Models on ESC50.",
    #     tags=["Environmental Sound Classification", "Fine-Tuning"],
    #     config=args,
    #     name=args.experiment_name
    # )

    device = torch.device('cuda') if args.cuda and torch.cuda.is_available() else torch.device('cpu')

    # model to preprocess waveform into mel spectrograms
    mel = AugmentMelSTFT(n_mels=args.n_mels,
                         sr=args.resample_rate,
                         win_length=args.window_size,
                         hopsize=args.hop_size,
                         n_fft=args.n_fft,
                         freqm=args.freqm,
                         timem=args.timem,
                         fmin=args.fmin,
                         fmax=args.fmax,
                         fmin_aug_range=args.fmin_aug_range,
                         fmax_aug_range=args.fmax_aug_range
                         )
    mel.to(device)

    # load prediction model
    pretrained_name = args.pretrained_name
    if pretrained_name:
        model = get_mobilenet(width_mult=NAME_TO_WIDTH(pretrained_name), pretrained_name=pretrained_name,
                              head_type=args.head_type, se_dims=args.se_dims, num_classes=3)
    else:
        model = get_mobilenet(width_mult=args.model_width, head_type=args.head_type, se_dims=args.se_dims,
                              num_classes=3)
    model.to(device)
     
    # dataloader
    dl = DataLoader(dataset=train_set,
                    worker_init_fn=worker_init_fn,
                    num_workers=args.num_workers,
                    batch_size=args.batch_size,
                    shuffle=True)

    # evaluation loader
    eval_dl = DataLoader(dataset=test_set,
                         worker_init_fn=worker_init_fn,
                         num_workers=args.num_workers,
                         batch_size=args.batch_size)

    # optimizer & scheduler
    lr = args.lr
    features_lr = args.features_lr if args.features_lr else lr
    classifier_lr = args.classifier_lr if args.classifier_lr else lr
    last_layer_lr = args.last_layer_lr if args.last_layer_lr else classifier_lr

    assert args.classifier_lr is None or args.last_layer_lr is None, "Either specify separate learning rate for " \
                                                                     "last layer or classifier, not both."

    optimizer = torch.optim.Adam([{'params': model.features.parameters(), 'lr': features_lr},
                                  {'params': model.classifier[:5].parameters(), 'lr': classifier_lr},
                                  {'params': model.classifier[5].parameters(), 'lr': last_layer_lr}
                                  ],
                                 lr=args.lr, weight_decay=args.weight_decay)
    # phases of lr schedule: exponential increase, constant lr, linear decrease, fine-tune
    schedule_lambda = \
        exp_warmup_linear_down(args.warm_up_len, args.ramp_down_len, args.ramp_down_start, args.last_lr_value)
    scheduler = torch.optim.lr_scheduler.LambdaLR(optimizer, schedule_lambda)

    name = None
    accuracy, val_loss = float('NaN'), float('NaN')

    print("\nTraining Start:")
    for epoch in range(args.n_epochs):
        mel.train()
        model.train()
        train_stats = dict(train_loss=list(),train_accu=list())
        pbar = tqdm(dl)
        pbar.set_description("\nEpoch {}/{}: accuracy: {:.4f}, val_loss: {:.4f}"
                             .format(epoch + 1, args.n_epochs, accuracy, val_loss))

        for batch in pbar:
            x,y = batch
            #print(x.size())
            bs = x.size(0)
            x, y = x.to(device), y.to(device)
            x = _mel_forward(x, mel)

            if args.mixup_alpha:
                rn_indices, lam = mixup(bs, args.mixup_alpha)
                lam = lam.to(x.device)
                x = x * lam.reshape(bs, 1, 1, 1) + \
                    x[rn_indices] * (1. - lam.reshape(bs, 1, 1, 1))
                y_hat, _ = model(x)
                samples_loss = (F.cross_entropy(y_hat, y, reduction="none") * lam.reshape(bs) +
                                F.cross_entropy(y_hat, y[rn_indices], reduction="none") * (
                                            1. - lam.reshape(bs)))

            else:
                y_hat, _ = model(x)  
                #print(y_hat)
                y_t=torch.from_numpy(np.zeros((len(x), 3)))
                for i in range(len(x)):
                    y_t[i][y[i]//3]+=1
                    
                samples_loss = F.cross_entropy(y_hat, y_t, reduction="none")
                #print(samples_loss)
           
            # loss & accuracy
            loss = samples_loss.mean()
            y_pre=((torch.sigmoid(y_hat))>=0.5).int()
            #print(y_pre)
            acc = metrics.accuracy_score(y_t.numpy(), y_pre.numpy())
            
            # append training statistics
            train_stats['train_loss'].append(loss.detach().cpu().numpy().item())
            train_stats['train_accu'].append(acc)
            
            # Update Model
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()
        # Update learning rate
        scheduler.step()
        print("Train loss ->", train_stats['train_loss'])
        print("Train acc ->", train_stats['train_accu'])
        # evaluate
        accuracy, val_loss = _test(model, mel, eval_dl, device)

        # log train and validation statistics
        # wandb.log({"train_loss": np.mean(train_stats['train_loss']),
        #            "features_lr": scheduler.get_last_lr()[0],
        #            "classifier_lr": scheduler.get_last_lr()[1],
        #            "last_layer_lr": scheduler.get_last_lr()[2],
        #            "accuracy": accuracy,
        #            "val_loss": val_loss
        #            })

        # remove previous model (we try to not flood your hard disk) and save latest model
        if name is not None:
             os.remove(os.path.join(name))
        name = f"mn{str(args.model_width).replace('.', '')}_urban_epoch_{epoch}_mAP_{int(round(accuracy*100))}.pt"
        torch.save(model.state_dict(), os.path.join(name))

#%%
def _mel_forward(x, mel):
    old_shape = x.size()
    x = x.reshape(-1, old_shape[2])
    x = mel(x)
    x = x.reshape(old_shape[0], old_shape[1], x.shape[1], x.shape[2])
    return x


def _test(model, mel, eval_loader, device):
    model.eval()
    mel.eval()

    targets = []
    outputs = []
    losses = []
    pbar = tqdm(eval_loader)
    pbar.set_description("Validating")
    for batch in pbar:
        x, y = batch
        x = x.to(device)
        y = y.to(device)
        with torch.no_grad():
            x = _mel_forward(x, mel)
            y_hat, _ = model(x)
        #print(y_hat)
        
        y_t=torch.from_numpy(np.zeros((len(x), 3)))
        for i in range(len(x)):
            y_t[i][y[i]//3]+=1
            
        targets.append(y_t.cpu().numpy())
        outputs.append(y_hat.float().cpu().numpy())
        losses.append(F.cross_entropy(y_hat, y_t).cpu().numpy())

    targets = np.concatenate(targets)
    outputs = np.concatenate(outputs)
    losses = np.stack(losses)
    
    y_pre=((1/(1+np.exp(-outputs)))>0.5).astype(int)
    accuracy = metrics.accuracy_score(targets,y_pre)
    
    return accuracy, losses.mean()

#%%
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Example of parser. ')

    # general
    parser.add_argument('--experiment_name', type=str, default="ESC50")
    parser.add_argument('--cuda', default=True )
    parser.add_argument('--batch_size', type=int, default=32)
    parser.add_argument('--num_workers', type=int, default=6)
    parser.add_argument('--fold', type=int, default=1)

    # training
    parser.add_argument('--pretrained_name', type=str, default="mn30_as")
    parser.add_argument('--model_width', type=float, default=3.0)
    parser.add_argument('--head_type', type=str, default="mlp")
    parser.add_argument('--se_dims', type=str, default="c")
    parser.add_argument('--n_epochs', type=int, default=40)
    parser.add_argument('--mixup_alpha', type=float, default=0.0)
    parser.add_argument('--roll', default=False, action='store_true')
    parser.add_argument('--gain_augment', type=float, default=0.0)
    parser.add_argument('--weight_decay', type=float, default=0.001)

    # lr schedule
    parser.add_argument('--lr', type=float, default=1e-5)
    # individual learning rates possible for classifier, features or last layer
    parser.add_argument('--classifier_lr', type=float, default=None)
    parser.add_argument('--last_layer_lr', type=float, default=None)
    parser.add_argument('--features_lr', type=float, default=None)
    parser.add_argument('--warm_up_len', type=int, default=10)
    parser.add_argument('--ramp_down_start', type=int, default=20)
    parser.add_argument('--ramp_down_len', type=int, default=20)
    parser.add_argument('--last_lr_value', type=float, default=0.01)

    # preprocessing
    parser.add_argument('--resample_rate', type=int, default=20500)
    parser.add_argument('--window_size', type=int, default=800)
    parser.add_argument('--hop_size', type=int, default=512)
    parser.add_argument('--n_fft', type=int, default=1024)
    parser.add_argument('--n_mels', type=int, default=128)
    parser.add_argument('--freqm', type=int, default=0)
    parser.add_argument('--timem', type=int, default=0)
    parser.add_argument('--fmin', type=int, default=0)
    parser.add_argument('--fmax', type=int, default=None)
    parser.add_argument('--fmin_aug_range', type=int, default=1)
    parser.add_argument('--fmax_aug_range', type=int, default=1000)

     
            
    args = parser.parse_args()
    train(args)