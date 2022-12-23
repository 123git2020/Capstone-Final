TODO: mention any differences when setting up in linux and windows

# Project directory
capstone-final/
├── README.md               # overview of the project
├── requirements.txt        # required dependencies
├── .gitignore              # ignored files
├── data/                   # audio files 
│   ├── database/           # live audio files
│   └── datasets/           # training datasets
└── src/                    # contains all code in the project
    ├── database/           # contains code for the postgres database
    ├── metrics/            # contains code for calculating metrics
    └── model/              # contains code for the model