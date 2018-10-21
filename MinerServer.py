'''
Reference:
    https://medium.com/@manivannan_data/how-to-get-data-received-in-flask-request-8ebadc2bb5c6
'''

from transaction import Transaction
from blockchain import Blockchain
from block import Block
from flask import Flask, jsonify, json, request, Response,send_from_directory
import time  
import hashlib 
import os
import pickle
from argparse import ArgumentParser  

UPLOAD_DIRECTORY = 'C:/Users/Li Yang/source/repos/BlockchainTechnology50037/BlockchainTechnology50037'  
app = Flask(__name__) 

parser = ArgumentParser()  
parser.add_argument('-H', '--host', default='127.0.0.1')  
parser.add_argument('-p', '--port', default=5000, type=int)
args = parser.parse_args()  

# @app.route('/create-transaction', methods = ['GET'])
# def get_transaction():
#     data = {
#        'Transaction'  : '',
#     }
#     js = json.dumps(data)
#     resp = Response(js, status=200, mimetype='application/json')
#     resp.headers['Link'] = 'http://luisrei.com'
#     return resp

# curl -H "Content-type: application/json" -X POST http://127.0.0.1:5000/create-transaction -d '{"sender":"1","receiver":"4s","amount":"45"}'
# requests.post('http://127.0.0.1:{}/create-transaction'.format(myId), headers={'Content-type': 'application/json'})
# TODO: Transaction can be sent as a string or python object
@app.route('/create-transaction', methods=['POST'])
def create_transaction():
    # Read JSON file
    for File in os.listdir("."):
        if File.endswith(".json"):
            with open('test_tx.json') as f:
                data = json.load(f)

	# Read request data
    if request.headers['Content-Type'] == 'text/plain':
	    myTx = request.data
    # elif request.headers['Content-Type'] == 'application/json':
        # newData = request.get_json()
        # newData = request.json
        # newData = json.dumps(newData)
        # print(newData)
        # myTx = {
        # 	"sender": newData["sender"],
        # 	"receiver": newData["receiver"],
        # 	"amount": newData["amount"],
        # }
        # myTx = Transaction.new(newData["sender"], newData["receiver"], newData["amount"], newData["privateKey"])
    # print(myTx)
    data["AllTransactions"].append(myTx)

    # Write JSON file
    with open('test_tx.json', 'w') as outfile:
	    json.dump(data, outfile)
    response = {
        'message': 'Transaction has been submitted successfully',
        # 'Signature': newData
    }
    # newData = json.dumps(newData)

    return jsonify(response), 201
    # return newData, 201

# TODO: Read from pending_transactions.JSON file
# @app.route('/read-transactions', methods=['GET'])
# def read_transactions():
# 	return

# @app.route('/get-header', methods = ['GET'])
# def get_header():
#     list_of_headers = []
#     with open("transaction_hash.json") as json_file:
#         data=json.load(json_file)
#     bc = Blockchain.new()
#     blockOne = Block(time.time(),bc.last_block.getHeaderInHash(),10,['123','456'])
#     proof = bc.proof_of_work(blockOne)
#     print(proof)
#     bc.add(blockOne,proof,"No",0)

#     blockTwo = Block(time.time(),bc.chain[-2].getHeaderInHash(),10,['abc','def'])
#     proofTwo = bc.proof_of_work(blockTwo)
#     print(proofTwo)
#     bc.add(blockTwo,proofTwo,"Yes",2)
#     print("Total Chain: " + str(bc.chain))
#     print("Forks: " + str(bc.fork.values()))
#     print("Resolve: " + str(bc.resolve()))
#     print("Length: " + str(len(bc.resolve())))
#     for block in bc.resolve():
#         print("Block: "+ str(block))
#         for attr, value in block.__dict__.items():
#             if(attr == "header"):
#                 print("Header: " + str(value))
#                 list_of_headers.append(value)
#     js = json.dumps(list_of_headers)
#     resp = Response(js, status=200, mimetype='application/json')
#     resp.headers['Link'] = 'http://luisrei.com'
#     return resp

# For SPVClients
# TODO: Read block header
@app.route('/read-block-header', methods=['GET'])
def read_block_header():
	return

# For checking who found a new nonce
@app.route('/read-blockchain-height', methods=['GET'])
def read_blockchain_length():
    f = open('./{}/blockchain'.format(args.port), 'rb').read()
    bc = pickle.load(f)
    f.close()
    height = len(bc.chain)
	return height

# GET blocks up to certain depth
@app.route('/read-block', methods=['GET'])
def read_block():
    # Read blockchain from binary
    f = open('./{}/blockchain'.format(args.port), 'rb').read()
    bc = pickle.load(f)
    # with open('data.pickle', 'rb') as f:
    # data = pickle.load(f)

    # Read args
    # blockHeader = request.args.get('header')
    blockHeaderHash = request.args['header']

    # iterate
    list_of_blocks = []
    height = len(bc.chain)
    for i in range(height):
        bc.chain[height - 1 - i]
    list_of_blocks = list(filter(lambda b: b!=self.myId, MINER_ADDR))          # Filter myId from all Ids      

	return

# @app.route('/mine/<path:filename>', methods = ['GET'])   
# def get_mine(filename):
#     return send_from_directory(UPLOAD_DIRECTORY, filename, as_attachment=True,attachment_filename='newFile')

@app.route('/update-blockchain', methods=['POST'])
def update_blockchain():
    if request.headers['Content-Type'] == 'application/octet-stream':
        f = open('./{}/blockchain'.format(args.port), 'wb')
        f.write(request.data)
        f.close()
        return "Binary message written!"
    else:
        return "415 Unsupported Media Type"

@app.route('/mine', methods = ['POST'])
def post_mine():
    if request.headers['Content-Type'] == 'application/octet-stream':
        f = open('./binary', 'wb')
        f.write(request.data)
        f.close()
        return "Binary message written!"
    else:
        return "415 Unsupported Media Type"

  
app.run(host=args.host, port=args.port, debug=True)
