# Store Stock Data from Yahoo Finance in CouchDB using Python

## Required Python Packages
```pip3 install bs4 # Beautiful Soup
pip3 install json # JSON Handling
pip3 install requests # for HTTP requests
pip3 install argparse # handle command line arguments
pip3 install hashlib # for unique filenames
```

## Usage
```make # see Makefile - recipes will correspond to each of the steps below```

Will run all steps and put the data in your CouchDB at `http://127.0.0.1:5984/`. Output from each step is stored in the `output` directory. Reference the `Makefile` to see how each individual step can be run. For example all `json` POSTed to CouchDB will be found in the `output/3` directory which corresponds to Step 3 below.

# Steps used to Fetch and Store the Stock Data
Using `python3` we will do the following:
0. Fetch all stock symbols from the Nasdaq FTP server at `ftp://ftp.nasdaqtrader.com/SymbolDirectory/nasdaqtraded.txt`
1. Reduce the symbols to exchange traded funds that also don't have $ or . in the names and build YQL queries for Yahoo finance
2. Query Yahoo finance and store the JSON. Note the query is from the `yahoo.finance.quotes` table.
3. Massage the Yahoo Finance JSON into CouchDB format and POST to CouchDB
4. Scrape Wikipedia for S&P 500 Stock Information
5. Merge S&P 500 Stock Information the CouchDB Data
5. Convert the CouchDB data to csv (comma separated values)

We store files from each step in the `output` folder.

## Querying Stock information from CouchDB

Consider the map function for CouchDB:

```
function(doc) {
    if (doc.DividendYield > 5.00 && doc.DividendYield < 6.00) {
        emit(doc._id,[doc.Name, doc.DividendYield]);
    }
}
```

This will return the symbol,name and DividendYield for all stocks that have a dividend yield from 5.00%-6.00%.
