all: couchdb-running clean step0-fetch-symbols step1-build-queries step2-query-yahoo-finance step3-store-stocks-couchdb

# From FTP fetch all traded symbols on the Nasdaq
step0-fetch-symbols:
	python3 0-fetch_nasdaq_symbols.py

# from the symbols (some filtered) build YQL queries to fetch from Yahoo Finance
step1-build-queries:
	python3 1-build_yql_queries.py

# query Yahoo with our YQL Queries and store JSON output
step2-query-yahoo-finance:
	python3 2-query_yahoo_api.py

# Post our JSON output from step 2 into CouchDb
step3-store-stocks-couchdb:
	python3 3-store_stocks_couchdb.py

# For OS X At least, more here for memory
couchdb-start:
	brew services start couchdb

# See in Fauxuton http://127.0.0.1:5984/_utils/
couchdb-running:
	curl http://127.0.0.1:5984/

clean:
	rm -rf output || true
