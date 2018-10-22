from blockchain import *
import requests
import pickle

myId = 5000
bc = Blockchain.new()
hasFound, newNonce, prevHeaderHash, minerId = bc.proof_of_work(bc.last_block, [])
bc.newAdd(Block(time.time(), prevHeaderHash, newNonce, ['123','abc']), newNonce)
hasFound, newNonce, prevHeaderHash, minerId = bc.proof_of_work(bc.last_block, [])
bc.newAdd(Block(time.time(), prevHeaderHash, newNonce, ['123','abc']), newNonce)
hasFound, newNonce, prevHeaderHash, minerId = bc.proof_of_work(bc.last_block, [])
bc.newAdd(Block(time.time(), prevHeaderHash, newNonce, ['123','abc']), newNonce)
hasFound, newNonce, prevHeaderHash, minerId = bc.proof_of_work(bc.last_block, [])
bc.newAdd(Block(time.time(), prevHeaderHash, newNonce, ['123','abc']), newNonce)
f = open('./{}/blockchain'.format(myId),'wb')
pickle.dump(bc,f)
f.close()
print(len(bc.chain))

# f = requests.get('http://127.0.0.1:{}/read-blockchain'.format(myId))
# myBlockchain = pickle.loads(f.content)
# print(myBlockchain)

# f = requests.get('http://127.0.0.1:{}/read-block-header'.format(myId))