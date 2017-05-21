# We will go through our S&P 500 JSON Data and merge it into CouchDB
import sys, argparse, os
import urllib.request
import requests
import json

numerrors = 0

def main(args):
  global numerrors
  chunklen=0
  symbols=[]
  sp500_json=args.infile.read()
  sp500_symbols=json.loads(sp500_json)
  args.infile.close()
  for symbol in sp500_symbols:
    url = args.couchdburl+symbol['_id']
    couchdbresponse = requests.get(url)
    if(couchdbresponse.status_code < 200 or couchdbresponse.status_code > 299):
      print("Missing CouchDB Data at url: %s" % url)
      numerrors = numerrors + 1
      continue

    stock = json.loads(couchdbresponse.text)
    new_stock = { **stock, **symbol }
    post_response = requests.put(url=url, json=new_stock)
    if(post_response.status_code < 200 or post_response.status_code > 299):
      print(post_response.text)
      numerrors = numerrors + 1

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Merge in S&P 500 Symbol Data to our data in CouchDB')
  parser.add_argument('-infile', type=argparse.FileType('r'), help='input file of json S&P 500 Data', default="output/4/sp500.json")
  parser.add_argument('-couchdburl', nargs="?", help='URL of our CouchDB Document Store', default="http://127.0.0.1:5984/stocks/")
  args = parser.parse_args()
  main(args)
  sys.exit(numerrors)

