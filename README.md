# Datemaker.py
Simple python script designed to be used as a CLI tool to calculate epochs given a starting datetime and list of deltas to apply

## Usage
```
$ ./datemaker.py -h

usage: datemaker.py [-h] [--start START_DATE_STRING] [--delta DELTA]

Make some epoch date ranges

optional arguments:
  -h, --help            show this help message and exit
  --start START_DATE_STRING, -s START_DATE_STRING
                        A string representing the date from which the deltas
                        should be applied. Date can be in the format "yyyy-mm-
                        dd" or "yyyy-mm-dd HH-MM-SS" Defaults to current
                        datetime if not specified
  --delta DELTA, -d DELTA
                        An integer representing a positive or negative amount
                        of 24-hour periods to adjust *start* by

```

#### Examples
```
# --start defaults to current datetime
$ ./datemaker.py -d -4 -d -10
>>> -4: 1498315779   # Sat Jun 24 14:49:39 UTC 2017
>>> -10: 1497797379  # Sun Jun 18 14:49:39 UTC 2017
```

```
$ ./datemaker.py --start 2017-06-01 -d +2 -d -3
>>> 2: 1496448000   # Sat Jun  3 00:00:00 UTC 2017
>>> -3: 1496016000  # Mon May 29 00:00:00 UTC 2017
```

```
$ ./datemaker.py --start "2017-03-01 12:12:12" -d +2 -d -3
>>> 2: 1488543132   # Fri Mar  3 12:12:12 UTC 2017
>>> -3: 1488111132  # Sun Feb 26 12:12:12 UTC 2017
```

## CLI Usage
Copy the `datemaker.py` file to be named whatever, make it an executable, and place it in you `PATH`

```
$ cp datemaker.py dm
$ chmod +x dm
$ mv dm $HOME/bin
$ which dm
>>> /home/username/bin/dm

$ dm -d +3 -d -4
>>> 3: 1498920208
>>> -4: 1498315408

```
