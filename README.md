# Puff
A Digital Forensics and Incident Response (DFIR) tool for Windows prefetch files analysis, filterable by date and json friendly.
Can be usefull in Incident Response (IR) or forensics cases, when you need to detect running program in a slice of time in a large set of prefetch files.

Created to work under Linux, but also on any system where there is python >= 3.10 




# INSTALL:
Clone project as usual ($ git clone https://github.com/massimiliano-dalcero/puff), enter inside directory ($ cd puff) and follow the next steps:

Assign execution permission to scripts:
```
$ chmod +x install.sh
$ chmod +x puff.sh
$ chmod +x puff.py
```

Exec the install.sh script (this create only python virtual env and install libraries with pip. All inside the current directory):
```
$ ./install.sh
```

Next: if you want this as system command:

copy directory in /usr/share/puff/  (or where you prefer)
run install.sh inside directory and then, create symbolic link to puff.sh in a system path:

```
# ln -s /usr/share/puff/puff.sh /usr/bin/puff
```

thats all :)


# HOW TO USE:

```
$ puff -h

usage: puff [-h] [--no-mapped] [--minimal] [-F FILTER] file.pf [file.pf ...]

Puff 1.0.1: An easy and JSON friendly Windows prefetch file parser based on pyscca library

positional arguments:
  file.pf               Windows prefetch file

options:
  -h, --help            show this help message and exit
  --no-mapped           Don't extract mapped file
  --minimal             Minimal output: only essential evidences
  -F FILTER, --filter FILTER
                        Last Run Date Filter: last_run > 2022-11-25 18:00:00 and last_run < 2022-11-26 02:00:00

```

An example of use:

```
$ puff --no-mapped -F "last_run >= 2022-10-15 19:00:00 and last_run < 2022-10-15 23:00:00" /mnt/C1/Windows/Prefetch/*
$ puff --minimal -F "last_run >= 2022-10-15 19:00:00 and last_run < 2022-10-15 23:00:00" /mnt/C1/Windows/Prefetch/*
```
