from transaction import Transaction
from blockchain import Blockchain
from block import Block
from flask import Flask, jsonify, json, request, Response,send_from_directory
import time  
import hashlib 
import os
import pickle

UPLOAD_DIRECTORY = 'C:/Users/Li Yang/source/repos/BlockchainTechnology50037/BlockchainTechnology50037'  
app = Flask(__name__) 

@app.route('/create-transaction', methods = ['GET'])
def get_transaction():
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

@app.route('/get-header', methods = ['GET'])
def get_header():
    list_of_headers = []
    with open("transaction_hash.json") as json_file:
        data=json.load(json_file)
    bc = Blockchain.new()
    blockOne = Block(time.time(),bc.last_block.getHeaderInHash(),10,['123','456'])
    proof = bc.proof_of_work(blockOne)
    print(proof)
    bc.add(blockOne,proof,"No",0)

    blockTwo = Block(time.time(),bc.chain[-2].getHeaderInHash(),10,['abc','def'])
    proofTwo = bc.proof_of_work(blockTwo)
    print(proofTwo)
    bc.add(blockTwo,proofTwo,"Yes",2)
    print("Total Chain: " + str(bc.chain))
    print("Forks: " + str(bc.fork.values()))
    print("Resolve: " + str(bc.resolve()))
    print("Length: " + str(len(bc.resolve())))
    for block in bc.resolve():
        print("Block: "+ str(block))
        for attr, value in block.__dict__.items():
            if(attr == "header"):
                print("Header: " + str(value))
                list_of_headers.append(value)
    js = json.dumps(list_of_headers)
    resp = Response(js, status=200, mimetype='application/json')
    resp.headers['Link'] = 'http://luisrei.com'
    return resp

@app.route('/get-proof', methods = ['GET'])   
def get_proof():
    pass

@app.route('/mine/<path:filename>', methods = ['GET'])   
def get_mine(filename):
    return send_from_directory(UPLOAD_DIRECTORY, filename, as_attachment=True,attachment_filename='newFile')

@app.route('/mine', methods = ['POST'])
def post_mine():
    if request.headers['Content-Type'] == 'application/octet-stream':
        f = open('./binary', 'wb')
        f.write(request.data)
        f.close()
        return "Binary message written!"
    else:
        return "415 Unsupported Media Type ;)"

from argparse import ArgumentParser  
parser = ArgumentParser()  
parser.add_argument('-H', '--host', default='127.0.0.1')  
parser.add_argument('-p', '--port', default=5000, type=int)  
args = parser.parse_args()  
  
app.run(host=args.host, port=args.port, debug=True)
