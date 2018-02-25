from flask import Flask
from flask_cors import CORS, cross_origin
from flask import jsonify
from bs4 import BeautifulSoup
from urllib.request import urlopen
from flask import Response, request
from flask_caching import Cache
import pandas as pdb
import json
import sys

app = Flask(__name__)
CORS(app)
cache = Cache(app, config={'CACHE_TYPE':'simple'})

@app.route("/",methods=['GET'])
def index():
    html = urlopen("http://stmt.nisoc.nioc")
    soup = BeautifulSoup(html.read(),"lxml")
    da1 = soup.find(id="lblLastPayrollStatement")
    da2 = soup.find(id="lblLastWagesStatement")
    return jsonify(statement1=da1.text, statement2=da2.text)


@app.route("/news",methods=['GET'])
def news():
    html = urlopen("http://portal.nisoc.ir")
    soup = BeautifulSoup(html.read(),"lxml")
    table = soup.find(id="{811209B8-6829-44D2-A021-E58BD8618F94}-{B4560F44-5A27-4853-B0BF-08A520953BBE}")
    table_rows = table.find_all('tr') 
    row = []   
    for tr in table_rows:
        td = tr.find_all('a', href=True)
        ro = {
                'val' : str(td[0].contents[0]).replace('"',''),
                'href': td[0]['href']
            }
        row.append(ro)
    jsonStr = json.dumps(row)
    
    table = soup.find(id="{590CD0C2-9290-4B0C-AF4F-DB1E118A5680}-{02E666CC-D3F7-4389-A9EE-6A5DA3F2D01D}")
    table_rows = table.find_all('tr') 
    row = []   
    for tr in table_rows:
        td = tr.find_all('a', href=True)
        ro = {
                'val' : str(td[0].contents[0]).replace('"',''),
                'href': td[0]['href']
            }
        row.append(ro)
    jsonStr1 = json.dumps(row)

    table = soup.find(id="{D699B009-5C20-4CFA-870B-D57FAE594D51}-{7A4C3967-13C4-4E73-B7E0-8C2A2C470641}")
    table_rows = table.find_all('tr') 
    row = []   
    for tr in table_rows:
        td = tr.find_all('a', href=True)
        try:
            ro = {
                'val' : str(td[0].contents[0]).replace('"',''),
                'href': td[0]['href']
            }
            row.append(ro)
        except Exception:
            print("")        
    jsonStr2 = json.dumps(row)
    return jsonify(Records=jsonStr, Records1=jsonStr1, Records2=jsonStr2)

@app.route("/mainnews",methods=['GET'])
def mainnews():
    html = urlopen("http://portal.nisoc.ir")
    soup = BeautifulSoup(html.read(),"lxml")
    table = soup.find(id="{D699B009-5C20-4CFA-870B-D57FAE594D51}-{7A4C3967-13C4-4E73-B7E0-8C2A2C470641}")
    table_rows = table.find_all('tr') 
    row = []   
    for tr in table_rows:
        td = tr.find_all('a', href=True)
        try:
            ro = {
                'val' : str(td[0].contents[0]).replace('"',''),
                'href': td[0]['href']
            }
            row.append(ro)
        except Exception:
            print("")        
    jsonStr = json.dumps(row)
    return jsonify(Records=jsonStr)

@app.route("/getlinkcontent/<path:url_portal>", methods=['GET'])
def getlinkcontent(url_portal):
    html = urlopen(url_portal)
    soup = BeautifulSoup(html.read(),"lxml")    
    return jsonify(str(soup))

@app.route("/getlinkcontent_Post/", methods=['POST'])
def getlinkcontent_Post():
    url = request.json["url_portal"]
    html = urlopen(url)
    soup = BeautifulSoup(html.read(),"lxml")    
    return jsonify(str(soup))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
