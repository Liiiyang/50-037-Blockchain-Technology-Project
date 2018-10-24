#TODO: Instantiate miners
#TODO: Instantiate forking miner
#TODO: Mining in infinite loop


from MinerClient import *
from transaction import *

'''
Create Blockchain
'''
c1 = 'Alice'
c2 = 'Bob'
c3 = 'Charlie'
myId = 5010
myId_One = 5000
myId_Two = 5010
sk1 = SigningKey.from_pem(open("./1/sk.pem".format(myId)).read())
# sk2 = SigningKey.from_pem(open("./2/sk.pem".format(myId)).read())
# sk3 = SigningKey.from_pem(open("./3/sk.pem".format(myId)).read())
sk_string = sk1.to_string()     # Shouldn't be a problem

tx1 = Transaction.new(c1, c2, 1, sk_string)
tx1 = tx1.to_json()
tx2 = Transaction.new(c2, c3, 1, sk_string)
tx2 = tx2.to_json()
tx3 = Transaction.new(c1, c3, 1, sk_string)
tx3 = tx3.to_json()

mc0 = Miner(5000)
mc1 = Miner(5010)
mc0_id = str(mc0.myId)
mc1_id = str(mc1.myId)

tx4 = Transaction.new(mc0_id, c1, 1, sk_string)
tx5 = Transaction.new(mc0_id, c2, 1, sk_string)
tx4 = tx4.to_json()
tx5 = tx5.to_json()

#bc = Blockchain.new()
#hasFound, newNonce, prevHeaderHash, minerId = bc.proof_of_work(bc.last_block, [])
#bc.newAdd(Block(time.time(), prevHeaderHash, newNonce, [tx4, tx5]), newNonce)
#hasFound, newNonce, prevHeaderHash, minerId = bc.proof_of_work(bc.last_block, [])
#bc.newAdd(Block(time.time(), prevHeaderHash, newNonce, [tx1, tx2]), newNonce)
#hasFound, newNonce, prevHeaderHash, minerId = bc.proof_of_work(bc.last_block, [])
#bc.newAdd(Block(time.time(), prevHeaderHash, newNonce, [tx3, tx4]), newNonce)
#hasFound, newNonce, prevHeaderHash, minerId = bc.proof_of_work(bc.chain[-2], [])
#bc.newAdd(Block(time.time(), prevHeaderHash, newNonce, [tx4, tx5]), newNonce,True,2)
#f = open('./{}/blockchain'.format(myId),'wb')
#pickle.dump(bc,f)
#f.close()

'''
Testing miners
'''

mc0 = Miner(myId_One)
mc1 = Miner(myId_Two)
blockChainOne = mc0.blockchain.new()
blockChainTwo = mc1.blockchain.new()
hasFound, newNonce, prevHeaderHash, minerId = blockChainOne.proof_of_work(blockChainOne.last_block, [])
blockChainOne.newAdd(Block(time.time(), prevHeaderHash, newNonce, [tx4, tx5]), newNonce)
blockChainTwo.newAdd(Block(time.time(), prevHeaderHash, newNonce, [tx4, tx5]), newNonce)

hasFound, newNonce, prevHeaderHash, minerId = blockChainOne.proof_of_work(blockChainOne.last_block, [])
blockChainOne.newAdd(Block(time.time(), prevHeaderHash, newNonce, [tx1, tx2]), newNonce)
blockChainTwo.newAdd(Block(time.time(), prevHeaderHash, newNonce, [tx1, tx2]), newNonce)

hasFound, newNonce, prevHeaderHash, minerId = blockChainOne.proof_of_work(blockChainOne.last_block, [])
blockChainOne.newAdd(Block(time.time(), prevHeaderHash, newNonce, [tx3, tx4]), newNonce)
blockChainTwo.newAdd(Block(time.time(), prevHeaderHash, newNonce, [tx3, tx4]), newNonce)

hasFound, newNonce, prevHeaderHash, minerId = blockChainOne.proof_of_work(blockChainOne.chain[-2], [])
blockChainOne.newAdd(Block(time.time(), prevHeaderHash, newNonce, [tx4, tx5]), newNonce,True,-2)
blockChainTwo.newAdd(Block(time.time(), prevHeaderHash, newNonce, [tx4, tx5]), newNonce,True,-2)


f = open('./{}/blockchain'.format(myId_One),'wb')
pickle.dump(blockChainOne,f)
f.close()
mc0.mine_block()

f = open('./{}/blockchain'.format(myId_Two),'wb')
pickle.dump(blockChainTwo,f)

mc1.mine_block()

