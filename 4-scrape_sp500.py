# we will scrape wikipedia for the s&p 500 and store the result in a json file
import sys, argparse, os
import urllib.request
import json
import requests
from bs4 import BeautifulSoup

WIKIPEDIA_S_AND_P_500_URL = "http://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

def main(args):
  page = urllib.request.urlopen(WIKIPEDIA_S_AND_P_500_URL).read()
  soup = BeautifulSoup(page,"html.parser")

  table = soup.find('table', {'class': 'wikitable sortable'})
  symbols = []
  for row in table.findAll('tr'):
    col = row.findAll('td')
    if len(col) > 0:
      symbol_data = dict()
      symbol = str(col[0].string.strip())
      symbol_data['_id'] = symbol
      symbol_data['Name'] = str(col[1].string)
      symbol_data['Sector'] = str(col[3].string.strip())
      symbol_data['Sub Industry'] = str(col[4].string.strip())
      symbol_data['City Headquarters'] = str(col[5].string)
      symbol_data['S&P Date Added'] = str(col[6].string)
      symbol_data['CIK'] = str(col[7].string.strip())
      symbol_data['S&P500'] = 1
      symbols.append(symbol_data)
  args.outfile.write(json.dumps(symbols))
  args.outfile.close()
if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Scrape a list of S&P 500 Companies and associated date from Wikipedia.org')
  parser.add_argument('-outfile', help='output file containing S&P 500 Symbols', default="sp500.json")
  parser.add_argument('--destdir', nargs="?", help='Directory to output to', default="output/4/")
  args = parser.parse_args()
  if not os.path.exists(args.destdir):
    os.makedirs(args.destdir)
  args.outfile=open(args.destdir+args.outfile,"w")
  main(args)

