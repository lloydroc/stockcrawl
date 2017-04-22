import urllib.request
import sys, argparse, os
import json
#Nasdaq Traded|Symbol|Security Name|Listing Exchange|Market Category|ETF|Round Lot Size|Test Issue|Financial Status|CQS Symbol|NASDAQ Symbol|NextShares
#0  - Nasdaq Traded
#1  - Symbol
#2  - Security Name
#3  - Listing Exchange
#4  - Market Category
#5  - ETF
#6  - Round Lot Size
#7  - Test Issue
#8  - Financial Status
#9  - CQS Symbol
#10 - NASDAQ Symbol
#11 - NextShares
URL="ftp://ftp.nasdaqtrader.com/SymbolDirectory/nasdaqtraded.txt"
def main(args):
  nasdaq_traded = urllib.request.urlopen(URL)
  header=True
  headers=[]
  stocks=[]
  for byte_line in nasdaq_traded:
    line = byte_line.decode('utf-8')
    args.fetchedfile.write(line)
    line = line.rstrip()
    if(line.find("File Creation Time") != -1): # at the last line
      break;
    data = line.split("|")
    if(header): # Header is on the first line
      header = False
      headers = data
    else:
      #if(data[5]=='N' and data[1].find(".") == -1 and data[1].find("$") == -1):
      #args.nasdaqjson.write(data[1]+"\n")
      d = dict(zip(headers,data))
      stocks.append(d)
  stocks_json = json.dumps(stocks, ensure_ascii=False, indent=2)
  args.jsonoutput.write(stocks_json)
  args.jsonoutput.close()
  args.fetchedfile.close()
if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Fetch traded stocks from '+URL)
  parser.add_argument('--fetchedfile', nargs="?", help='Fetched nasdaqtraded file', default="nasdaqtraded.txt")
  parser.add_argument('--jsonoutput', nargs="?", help='Nasdaq Traded file in JSON format', default="nasdaqtraded.json")
  parser.add_argument('--destdir', nargs="?", help='Directory to output to', default="output/0/")
  args = parser.parse_args()
  if not os.path.exists(args.destdir):
    os.makedirs(args.destdir)
  args.jsonoutput=open(args.destdir+args.jsonoutput,"w")
  args.fetchedfile=open(args.destdir+args.fetchedfile,"w")
  main(args)

