ShowWords
=========

Show words and translations on your HDTV from your Google Spreadsheet.
How it will look like see http://youtu.be/BtGnvZQzcws

Supported for Ubuntu. Tested on Ubuntu 13.10

# Setup
Clone by
```bash
git clone git@github.com:artgo/ShowWords.git
```

Install libraries by running
```bash
cd ShowWords
./install.sh
```

1. Edit your email and password for your Gmail account in file pass.txt;
2. Edit your Google Spreadsheet filename in ```spreadsheet_file_name``` variable in file words.py. 

# Run
```bash
./words.py
```

You can also create a symbolic link to it and put it on your desktop or add the program to startup.
