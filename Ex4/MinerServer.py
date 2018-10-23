from Transaction import Transaction
from blockchain import Blockchain
from block import Block
from flask import Flask, jsonify, json, request, Response,send_from_directory
from argparse import ArgumentParser  
import time  
import hashlib 
import os
import pickle

UPLOAD_DIRECTORY = 'C:/Users/Li Yang/source/repos/BlockchainTechnology50037/BlockchainTechnology50037'  
app = Flask(__name__) 

parser = ArgumentParser()  
parser.add_argument('-H', '--host', default='127.0.0.1')  
parser.add_argument('-p', '--port', default=5000, type=int)
args = parser.parse_args()  

# Example command:
# python3 MinerServer.py -p 5000

# requests.post('http://127.0.0.1:{}/create-transaction'.format(myId), json=myTxJSON ,headers=headers)
# TODO: Done. Transaction can be sent as a string or python object
@app.route('/create-transactions', methods=['POST'])
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
    data["AllTransactions"] = []
    with open('pending_transactions.json', 'w') as outfile:
        json.dump(data, outfile)
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
        print(height)
        ls = []
        for b in bc.chain:
            print(b)
            ls.append(b.header)
    resp = pickle.dumps(ls)
    return Response(resp)

@app.route('/read-tx-and-proof', methods = ['GET'])
def read_tx_proof():
    # Open blockchain file
    all_my_transactions = []
    all_my_txProofs = []
    length = int(request.args['length'])
    receiver = request.args['receiver']
    with open('./{}/blockchain'.format(args.port), 'rb') as f:
        bc = pickle.load(f)
        depthOfBlocks = bc.chain[length:]
        for currentBlock in depthOfBlocks:
            print("Tx: " + str(currentBlock.transactions))
            for tx in currentBlock.transactions:
                print("tx: " + str(tx))
                #Or Bob's public key
                if Transaction.from_json(tx)["receiver"] == receiver: 
                    all_my_transactions.append(tx)             
            for myTx in all_my_transactions:
                txProof = currentBlock.get_merkleProofs(myTx)
                all_my_txProofs.append(txProof)
    data = {
        "Transactions": all_my_transactions,
        "Proofs": all_my_txProofs
        }
    resp = pickle.dumps(data)
    return Response(resp)

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
    # jHeight = jsonify(height)
    jHeight = json.dumps(height)
    return Response(jHeight)



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
        # list_of_blocks.append(b)            # [43, 42, 41]
        list_of_blocks = [b] + list_of_blocks
        # list_of_blocks = [b] + list_of_blocks
        if b.header['prevHeaderHash'] == blockHeaderHash:
            break
    resp = pickle.dumps(list_of_blocks)
    return Response(resp)

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