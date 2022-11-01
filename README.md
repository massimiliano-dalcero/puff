# Puff
An easy and json friendly Windows prefetch file parser filterable by date.

Can be usefull in Incident Response (IR) or forensics cases, when you need to detect running program in a slice of time in a large set of prefetch files.

Created to work under Linux, but also on any system where there is python >= 3.10 




# INSTALL:
clone project and inside directory 

```
$ chmod +x install.sh
$ chmod +x puff.sh
$ chmod +x puff.py
```

exec the install.sh script (this create only python virtual env and install libraries with pip. All inside the current directory):
```
$ ./install.sh
```

Next, if you want this as system command:

copy directory in (eg) /usr/share/puff/

and then create symbolic link to puff.sh:

```
# ln -s /usr/share/puff/puff.sh /usr/bin/puff
```

thats all :)


# HOW TO USE:

```
$ puff -h

usage: puff [-h] [--no-mapped] [-F FILTER] file.pf [file.pf ...]

Puff 1.0: An easy and JSON friendly Windows prefetch file parser based on pyscca library

positional arguments:
  file.pf               Windows prefetch file

options:
  -h, --help            show this help message and exit
  --no-mapped           Don't extract mapped file
  -F FILTER, --filter FILTER
                        Last Run Date Filter: last_run > 2022-11-25 18:00:00 and last_run < 2022-11-26 02:00:00
```

An example of use:

```
$ puff --no-mapped -F "last_run > 2022-10-15 19:00:00 and last_run < 2022-10-15 23:00:00" /mnt/C1/Windows/Prefetch/*
```
