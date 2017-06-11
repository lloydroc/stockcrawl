# We will go through the text file containing stock symbols and create
# YQL queries of the form
# select * from yahoo.finance.quotes where symbol in ("AAPL","T")
# but make the number of tickers in the in statement to have 
# around 1600 bytes. The reason for this is a URL can "sort of"
# have a length of maximum 2000 bytes
# later we will take the output file of YQL queries and
# do curl requests to get data back
import sys, argparse, os
import json
YQL_QUERY_FRONT="select * from yahoo.finance.quotes where symbol in ("
MAXCHUNKLEN=1600
queries=[]

def main(args):
  chunklen=0
  symbols=[]
  nasdaq_json=args.infile.read()
  obj=json.loads(nasdaq_json)
  for stock in obj:
    symbol = stock["Symbol"]
    nonetf = stock["ETF"]=="N"
    if nonetf and symbol.find("$") == -1: # filter out non ETF and $ in the symbol
      nextticker='"%s"' % (symbol)
      symbols.append(nextticker)
      chunklen+=len(nextticker)
    if(chunklen>=MAXCHUNKLEN):
      addYqlQuery(symbols)
      symbols=[]
      chunklen=0
  addYqlQuery(symbols) # write out the last one
  args.infile.close()
  args.outfile.write("\n".join(queries))
  args.outfile.close()
def addYqlQuery(symbols):
  if(len(symbols)>0):
    tickerlist = ",".join(symbols)
    queries.append(YQL_QUERY_FRONT+tickerlist+")")
if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Convert a list of stock symbols (a.k.a tickers) into Yahoo YQL Queries')
  parser.add_argument('-infile', type=argparse.FileType('r'), help='input file of symbols stock symbols in json', default="output/0/nasdaqtraded.json")
  parser.add_argument('-outfile', help='output file containing Yahoo YQL Queries', default="yql-queries.txt")
  parser.add_argument('--destdir', nargs="?", help='Directory to output to', default="output/1/")
  args = parser.parse_args()
  if not os.path.exists(args.destdir):
    os.makedirs(args.destdir)
  args.outfile=open(args.destdir+args.outfile,"w")
  main(args)

