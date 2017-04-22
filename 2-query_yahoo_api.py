import requests
import sys, argparse
import os
import hashlib
import json
YAHOO_API_URL="https://query.yahooapis.com/v1/public/yql"
YAHOO_API_PARAMS={"format":"json","env":"store%3A%2F%2Fdatatables.org%2Falltableswithkeys"}
def main(args):
  for yqlquery in args.infile:
    filename=hashlib.md5(yqlquery.encode('utf-8')).hexdigest()
    yqlquery = yqlquery.rstrip()
    yqlquery=yqlquery.replace(" ","%20")
    yqlquery=yqlquery.replace('"',"%22")
    query = {"q":yqlquery}
    params = {**query,**YAHOO_API_PARAMS} # requires python 3.5
    payload_str = "&".join("%s=%s" % (k,v) for k,v in params.items()) # default url encoding will break it
    r = requests.get(YAHOO_API_URL,params=payload_str)
    result = r.json()
    q = result["query"]["results"]["quote"]
    json.dump(q, open("%s/%s.json" % (args.outdir,filename),'w'),indent=2)
  args.infile.close()
if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Fetch data from a list YQL Queries and save to files')
  parser.add_argument('--infile', type=argparse.FileType('r'), help='input file of YQL Queries',default="output/1/yql-queries.txt")
  parser.add_argument('--outdir', help='Output directory for YQL query responses',default="output/2/")
  args = parser.parse_args()
  if not os.path.exists(args.outdir):
    os.makedirs(args.outdir)
  main(args)
