# Store Stock Data from Yahoo Finance in CouchDB using Python3

## Required Python Packages
There are a number of packages used from `python3` we need.

```
pip3 install bs4 # Beautiful Soup
pip3 install json # JSON Handling
pip3 install requests # for HTTP requests
pip3 install argparse # handle command line arguments
pip3 install hashlib # for unique filenames
```

## Usage
From the command line run:

```
make # see Makefile it's very simple on how to run each of the 4 steps below
```

Will run all steps and put the data in your CouchDB at `http://127.0.0.1:5984/`. Output from each step is stored in the `output` directory. Reference the `Makefile` to see how each individual step can be run. For example all `json` POSTed from `Step 3` to CouchDB will be found in the `output/3` directory.

# Steps used to Fetch and Store the Stock Data
Using `python3` we will do the following:

0. Fetch all stock symbols from the Nasdaq FTP server at `ftp://ftp.nasdaqtrader.com/SymbolDirectory/nasdaqtraded.txt`
1. Reduce the symbols to exchange traded funds that also don't have $ or . in the symbol name (e.g. stock ticker) and build YQL queries for Yahoo finance
2. Query Yahoo finance and store the JSON. Note the query is from the `yahoo.finance.quotes` table.
3. Massage the Yahoo Finance JSON into CouchDB format and POST to CouchDB

We store files from each step in the `output` folder.
