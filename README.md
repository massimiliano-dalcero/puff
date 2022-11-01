# Puff
An easy and json friendly Windows prefetch file parser filterable by date

Created to work under linux, but also on any system where there is python 3.10


# INSTALL:
clone project and inside directory 

```
$ chmod +x install.sh
$ chmod +x puff.sh
$ chmod +x puff.py
```

exec the install.sh script:
```
$ ./install.sh
```

Next, if you want this as system command:

copy directory in (eg) /usr/share/puff/

and then create symbolic link to puff.sh:

```
# ln -s /usr/share/puff/puff.sh /usr/bin
```

thats all :)


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

