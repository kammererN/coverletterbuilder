# Cover Letter Builder

A suite of Python tools for generating cover letters and applying to positions via email.

This tool is specifically designed to speed up the process of applying to vacancies on the StateJobsNY portal.

## How to Use

Simply download the binary, provided for Unix-based systems (i.e. Linux & MacOS). Currently, binaries for the Windows version are not available, although it can be easily compiled using this source code. 

After downloading the appropriate binary, run the following for a list of commands:

```bash
./clettrbuildr --help
```

The two important files for this program are ```config.json``` and ```texvars.json```, both of which are expected in the same directory as the binary (*Change this*).

### Config.json

This json file is the main configuration of the program. Most names should be self-explanatory, but they will be explained below. The expected structure of the json object is as follows:

```json
{
    "writer": {
        "texvars_path": "/path/to/texvars.tex"
    },
    "builder": {
        "texfile_dir": "/path/to/tex",
        "texfile": "/path/to/coverletter.tex",
        "output_dir": "/path/to/.output",
        "output_filename": "CoverLetter",
        "builds_dir": "/path/to/pdf"
    },
    "mailer": {
        "sender_email": "Email address to be sent from",
        "sender_password": "The password for the address above",
        "smtp_server_address": "Default: smtp.gmail.com",
        "smtp_port": "Default: 587",
        "attachments": [
            "/path/to/CoverLetter.pdf",
            "/path/to/Resume.pdf"
        ]
    },
    "db": {
        "datafile_path": "/path/to/db.csv"
    }
}
```

### Texvars.json

This json file controls several text variables to be written into a tex file. The expected structure of the json object is as follows:

```json
{
    "stateAgency": "The state agency being applied to",
    "vacancyID": "The vacancy ID for this position",
    "hiringManager": "The name of the hiring manager for this position",
    "vacancyTitle": "The title for this position",
    "theirStreetNumber": "The street number of the hiring contact",
    "theirCityStateZip": "The city-state-zip of the hiring contact",
    "theirEmailAddress": "The email address of the hiring contact"
}
```
