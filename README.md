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
$ pip install -r requirements.txt

# Windows
> pip install -r requirements.txt
```

## Project Structure
```
capstone-final/
├── README.md               # overview of the project
├── requirements.txt        # required dependencies
├── .gitignore              # ignored files
├── data/                   # audio files 
│   ├── database/           # live audio files
│   └── datasets/           # training datasets
└── src/                    # contains all code in the project
    ├── database/           # contains code for the postgres database
    ├── datasets/           # contains code for homogenizing the training datasets
    ├── metrics/            # contains code for calculating metrics
    └── model/              # contains code for the model
```

## Datasets
`cityCar28.wav` from Isolated Urban Sound Database was removed as it doesn't have any sounds in it. 
