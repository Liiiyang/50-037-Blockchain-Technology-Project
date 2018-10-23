'''
Reference:
    https://medium.com/@manivannan_data/how-to-get-data-received-in-flask-request-8ebadc2bb5c6
'''

# from blockchain import Blockchain
# from block import Block
from flask import Flask, jsonify, json, request, Response,send_from_directory
import time  
import hashlib 
import os
import pickle
from argparse import ArgumentParser  
from blockchain import Blockchain

UPLOAD_DIRECTORY = 'C:/Users/Li Yang/source/repos/BlockchainTechnology50037/BlockchainTechnology50037'  
app = Flask(__name__) 

parser = ArgumentParser()  
parser.add_argument('-H', '--host', default='127.0.0.1')  
parser.add_argument('-p', '--port', default=5000, type=int)
args = parser.parse_args()  

# Example command:
# python3 MinerServer.py -p 5000

# @app.route('/create-transaction', methods = ['GET'])
# def get_transaction():
#     data = {
#        'Transaction'  : '',
#     }
#     js = json.dumps(data)
#     resp = Response(js, status=200, mimetype='application/json')
#     resp.headers['Link'] = 'http://luisrei.com'
#     return resp

# requests.post('http://127.0.0.1:{}/create-transaction'.format(myId), json=myTxJSON ,headers=headers)
# TODO: Done. Transaction can be sent as a string or python object
@app.route('/create-transaction', methods=['POST'])
def create_transaction():
    # Read JSON file
    for File in os.listdir("."):
        if File.endswith(".json"):
            with open('pending_transactions.json') as f:
                data = json.load(f)

	# Read request data
    if request.headers['Content-Type'] == 'text/plain':
	    myTx = request.data
    elif request.headers['Content-Type'] == 'application/json':
        myTx = request.get_json()
        # newData = request.json
        # newData = json.dumps(newData)
        # print(newData)
        # myTx = {
        # 	"sender": newData["sender"],
        # 	"receiver": newData["receiver"],
        # 	"amount": newData["amount"],
        # }
        # myTx = Transaction.new(newData["sender"], newData["receiver"], newData["amount"], newData["privateKey"])
    print(myTx)
    data["AllTransactions"].append(myTx)

    # Write JSON file
    with open('pending_transactions.json', 'w') as outfile:
	    json.dump(data, outfile)
    response = {
        'message': 'Transaction has been submitted successfully',
        # 'Signature': newData
    }
    # newData = json.dumps(newData)

    return jsonify(response), 201
    # return newData, 201


# TODO: Read from pending_transactions.JSON file
# requests.get('http://127.0.0.1:{}/read-transaction'.format(myId))
@app.route('/read-transactions', methods=['GET'])
def read_transactions():
    for File in os.listdir("."):
        if File.endswith(".json"):
            with open('pending_transactions.json') as f:
                data = json.load(f)
    resp = data
    # TODO: delete
    # data["AllTransactions"] = []
    # with open('pending_transactions.json', 'w') as outfile:
    #     json.dump(data, outfile)
    return jsonify(resp)


# f = requests.get('http://127.0.0.1:{}/read-blockchain'.format(myId))
# myBlockchain = pickle.loads(f.content)
# TODO: Done
@app.route('/read-blockchain', methods=['GET'])
def read_blockchain():
    path = './{}'.format(args.port)
    if os.path.getsize(path+'/blockchain') == 0:
        return '', 202
    else:
        return send_from_directory(path,'blockchain')
    # for File in os.listdir("./{}".format(args.port)):
    #     print(File)
    #     if File == "blockchain":
    #         return send_from_directory('./{}'.format(args.port),'blockchain')
    #     else:
    #         return '', 202

# For SPVClients
# f = requests.get('http://127.0.0.1:{}/read-block-header'.format(myId), params={'depth': 1})
# TODO: Done
@app.route('/read-block-header', methods=['GET'])
def read_block_header():
    depth = int(request.args['depth'])
    with open('./{}/blockchain'.format(args.port), 'rb') as f:
        bc = pickle.load(f)
    height = len(bc.chain)
    ls = []
    for b in bc.chain[height-depth:]:
        ls.append(b.header)
    return jsonify(ls)


# For checking who found a new nonce
# TODO: Done
@app.route('/read-blockchain-height', methods=['GET'])
def read_blockchain_length():
    with open('./{}/blockchain'.format(args.port), 'rb') as f:
        bc = pickle.load(f)
    # f = open('./{}/blockchain'.format(args.port), 'rb').read()
    # bc = pickle.load(f)
    # f.close()
    height = len(bc.chain)
    return jsonify(height)



# GET blocks up to headerhash. Inclusive of block with requested prevHeaderHash
# TODO: Done
@app.route('/read-blocks-from-winner', methods=['GET'])
def read_blocks_from_winner():
    with open('./{}/blockchain'.format(args.port), 'rb') as f:
        bc = pickle.load(f)
    # Read args
    blockHeaderHash = request.args['header']
    print(blockHeaderHash)
    # iterate
    list_of_blocks = []
    height = len(bc.chain)
    for i in range(height):
        b = bc.chain[height - 1 - i]
        list_of_blocks.append(b)
        if b.header['prevHeaderHash'] == blockHeaderHash:
            break
    resp = pickle.dumps(list_of_blocks)
    return Response(resp)

# Deprecated
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



# Deprecated: Use local write instead
# @app.route('/update-blockchain', methods=['POST'])
# def update_blockchain():
#     if request.headers['Content-Type'] == 'application/octet-stream':
#         f = open('./{}/blockchain'.format(args.port), 'wb')
#         f.write(request.data)
#         f.close()
#         return "Binary message written!"
#     else:
#         return "415 Unsupported Media Type"

# Deprecated
# @app.route('/mine', methods = ['POST'])
# def post_mine():
#     if request.headers['Content-Type'] == 'application/octet-stream':
#         f = open('./binary', 'wb')
#         f.write(request.data)
#         f.close()
#         return "Binary message written!"
#     else:
#         return "415 Unsupported Media Type"

  
app.run(host=args.host, port=args.port, debug=True)
