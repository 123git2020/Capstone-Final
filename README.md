# Audio Classifier
TODO: venv setup for windows

Note: Development is currently being done in Linux so the instructions for Windows may not be completely correct. Currently only works with a local version of the postgres database. 

## Requirements
Linux or Windows. Python 3.6 or higher is needed.

## Quickstart
1. Set up a virtual environment.
```
# Linux
$ python -m venv venv
$ source venv/bin/activate

# Windows
> python -m venv venv
```

2. Install required dependencies.
```
# Linux
$ sudo apt-get install libpq-dev python3.x-dev          # replace the x with the version of python you're using
$ sudo apt-get install libportaudio2
$ pip install -r requirements.txt

# Windows
> pip install -r requirements.txt
```

3. Download the fine-tune trained model [Fine-tuned BEATs_iter3+ (AS2M) (cpt2)](https://msranlcmtteamdrive.blob.core.windows.net/share/BEATs/BEATs_iter3_plus_AS2M_finetuned_on_AS2M_cpt2.pt?sv=2020-08-04&st=2022-12-18T10%3A41%3A16Z&se=3022-12-19T10%3A41%3A00Z&sr=b&sp=r&sig=gSSExKP0otwVBgKwdV8FoMWL2VppARFq%2B26xKin5rKw%3D) and put it in the `src/model/beats` directory.

## Project Structure
```
capstone-final/
├── README.md               # overview of the project
├── requirements.txt        # required dependencies
├── .gitignore              # ignored files
├── m3_demo.py              # milestone 3 demo
├── audio/                  # temporary storage for audio files in milestone 3
├── data/                   # audio files 
│   ├── database/           # live audio files
│   └── datasets/           # training datasets
└── src/                    # contains all code in the project
    ├── database/           # contains code for the postgres database
    ├── datasets/           # contains code for homogenizing the training datasets
    ├── metrics/            # contains code for calculating metrics
    └── model/              # contains code for the model
        └── beats/          # contains code for the BEATs model
    
```

## Datasets
`cityCar28.wav` from Isolated Urban Sound Database was removed as it doesn't have any sounds in it. 

## Classification Models
BEATs is currently being used. The repository can be found [here](https://github.com/microsoft/unilm/tree/master/beats) and the paper can be found [here](https://arxiv.org/abs/2212.09058).
