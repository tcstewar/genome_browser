# genome_browser
Helper tools for a genome browser


# Requirements

- Python
- numpy
- bx-python  https://bitbucket.org/james_taylor/bx-python/wiki/HowToInstall
  - Install with easy_install https://bitbucket.org/james_taylor/bx-python/get/tip.tar.bz2
  - Seems to only work on Linux 


# How to run the JSON server

 - go into this directory
 - python server.py

A server will start on port 8080 and a web browser window should pop up to
access it.  There are basic web pages to list the available .bw files
and their contents.  The actual JSON query is of this form:


http://localhost:8080/query?name=Npas4_Npas4_KCl_B1_E120.bw&c=chr1&start=0&end=197195432&count=2

The arguments are:
 - name (the filename of the .bw file)
 - c (the chromosome name/id inside to .bw file)
 - start (the index to start at)
 - end (the index to end at)
 - count (the number of data points to return)

The result is a JSON file in the following format:

[{"max": 14.984169960021973, 
  "min": 0.13030000030994415, 
  "std_dev": 0.15074256104681408, 
  "coverage": 0.28205121911748948, 
  "mean": 0.17770868454590835}, 
 {"max": 11.857040405273438, 
  "min": 0.13030000030994415, 
  "std_dev": 0.14534401287063992, 
  "coverage": 0.31548349456695324, 
  "mean": 0.17771984602818136}]

For each data point, there is a max, a min, a mean, a standard deviation, 
and a coverage value (the percentage of data that is present).  If no
data is present for a data point, max will be -inf, min will be inf,
std_dev and mean will be NaN, and coverage will be 0.
