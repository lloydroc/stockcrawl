#!/usr/bin/python
import sys, argparse, os, csv, json
import requests

ALL_STOCKS = "http://127.0.0.1:5984/stocks/_all_docs"

def write_csv(args,all_stocks):
  output = csv.writer(args.outfile)
  first_stock = requests.get(url='http://127.0.0.1:5984/stocks/A')
  cols = json.loads(first_stock.text).keys()
  cols = sorted(cols)
  cols.remove("_id");
  cols = ['_id'] + cols
  output.writerow(cols)
  #delta = get_delta_data()
  for symbol in all_stocks:
    resp = requests.get(url='http://127.0.0.1:5984/stocks/'+symbol)
    data = json.loads(resp.text)
    # only 500 stocks have S&P 500 Data
    # so we have to merge in the missing columns
    row = []
    for col in cols:
      if(col == 'MarketCapitalization' and col in data):
        if(data[col]):
          mul = 1.0
          d = 1.0
          if 'B' in data[col]:
            mul = 1e9
            d = float(data[col].replace('B',''))
          elif 'M' in data[col]:
            mul = 1e6
          d = str(data[col]).replace('M','').replace('B','')
          row.append(float(d)*mul)
        else:
          row.append(0.00)
      elif(col in data):
        row.append(data[col])
      else:
        row.append('')
    output.writerow(row)
  args.outfile.close()
  return symbols
def get_all_stocks():
  symbols = []
  all_stocks = requests.get(url='http://127.0.0.1:5984/stocks/_all_docs')
  for symbol in all_stocks.json()['rows']:
    if(not symbol['id'].startswith('_')):
      symbols.append(symbol['id'])
  return symbols
def get_delta_data():
  delta = {}
  delta['Sector'] = ''
  delta['Sub Industry'] = ''
  delta['City Headquarters'] = ''
  delta['S&P Date Added'] = ''
  delta['CIK'] = ''
  delta['S&P500'] = 0
  return delta

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Convert all stock data in CouchDB to a CSV file')
  parser.add_argument('--outfile', help='Output CSV Filename', default="stocks.csv")
  parser.add_argument('--outdir', help='Output directory for YQL query responses',default="output/6/")
  args = parser.parse_args()
  if not os.path.exists(args.outdir):
    os.makedirs(args.outdir)
  args.outfile=open(args.outdir+args.outfile,"w")
  symbols = get_all_stocks()
  write_csv(args,symbols)
