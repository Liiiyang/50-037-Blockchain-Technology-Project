from transaction import Transaction
import time  
import hashlib 
from flask import Flask, jsonify, json, request, Response
  
app = Flask(__name__) 

@app.route('/create-transaction', methods = ['GET'])
def test():
    data = {
       'Transaction'  : '',
    }
    js = json.dumps(data)
    resp = Response(js, status=200, mimetype='application/json')
    resp.headers['Link'] = 'http://luisrei.com'
    return resp

@app.route('/create-transaction', methods=['POST'])  
def new():
    newData = request.json
    print("Data: " + str(newData))
    response = {
        'message': 'Transaction has been submitted successfully',
        'Signature': newData
        }
    return jsonify(response), 201

from argparse import ArgumentParser  
parser = ArgumentParser()  
parser.add_argument('-H', '--host', default='127.0.0.1')  
parser.add_argument('-p', '--port', default=5000, type=int)  
args = parser.parse_args()  
  
app.run(host=args.host, port=args.port, debug=True)