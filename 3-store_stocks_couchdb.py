import requests
import sys, argparse
import os
from os import listdir
from os.path import isfile, join
import hashlib
import json
COUCHDB_URL="http://127.0.0.1:5984/stocks/_bulk_docs"
def main(args):
  jsonfiles = [f for f in listdir(args.indir) if isfile(join(args.indir, f))]
  for jsonfile in jsonfiles:
    fd=open(args.indir+"/"+jsonfile,"r")
    jsonStr=fd.readlines()
    jsonStr="".join(jsonStr)
    jsonStr=jsonStr.replace('"symbol":','"_id":')
    fd.close()
    newjsonStr=[]
    newjsonStr.append('{"docs":')
    newjsonStr.append(jsonStr)
    newjsonStr.append('}')
    newjsonStr="".join(newjsonStr)
    newfilename="%s.json"%(hashlib.md5(newjsonStr.encode('utf-8')).hexdigest())
    fd=open(args.outdir+newfilename,"w")
    fd.write(newjsonStr)
    fd.close()
    requests.post(COUCHDB_URL,json=json.loads(newjsonStr))
if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Post data into CouchDB from a list YQL Query responses, also save to files')
  parser.add_argument('--indir', help='Directory to read YQL Query response from',default="output/2/")
  parser.add_argument('--outdir', help='Output directory of json stored in CouchDb',default="output/3/")
  args = parser.parse_args()
  if not os.path.exists(args.outdir):
    os.makedirs(args.outdir)
  main(args)
