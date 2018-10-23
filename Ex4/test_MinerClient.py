from MinerClient import *
from Transaction import *


'''
Create Blockchain
'''
c1 = 'Alice'
c2 = 'Bob'
c3 = 'Charlie'
myId = 5010
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

bc = Blockchain.new()
hasFound, newNonce, prevHeaderHash, minerId = bc.proof_of_work(bc.last_block, [])
bc.newAdd(Block(time.time(), prevHeaderHash, newNonce, [tx4, tx5]), newNonce)
hasFound, newNonce, prevHeaderHash, minerId = bc.proof_of_work(bc.last_block, [])
bc.newAdd(Block(time.time(), prevHeaderHash, newNonce, [tx1, tx2]), newNonce)
hasFound, newNonce, prevHeaderHash, minerId = bc.proof_of_work(bc.last_block, [])
bc.newAdd(Block(time.time(), prevHeaderHash, newNonce, [tx3, tx4]), newNonce)
hasFound, newNonce, prevHeaderHash, minerId = bc.proof_of_work(bc.last_block, [])
bc.newAdd(Block(time.time(), prevHeaderHash, newNonce, [tx4, tx5]), newNonce)
hasFound, newNonce, prevHeaderHash, minerId = bc.proof_of_work(bc.last_block, [])
bc.newAdd(Block(time.time(), prevHeaderHash, newNonce, [tx3, tx4]), newNonce)
hasFound, newNonce, prevHeaderHash, minerId = bc.proof_of_work(bc.last_block, [])
bc.newAdd(Block(time.time(), prevHeaderHash, newNonce, [tx4, tx5]), newNonce)
hasFound, newNonce, prevHeaderHash, minerId = bc.proof_of_work(bc.last_block, [])
bc.newAdd(Block(time.time(), prevHeaderHash, newNonce, [tx3, tx4]), newNonce)
hasFound, newNonce, prevHeaderHash, minerId = bc.proof_of_work(bc.last_block, [])
bc.newAdd(Block(time.time(), prevHeaderHash, newNonce, [tx4, tx5]), newNonce)
f = open('./{}/blockchain'.format(myId),'wb')
pickle.dump(bc,f)
f.close()

'''
Testing miners
'''

# mc0 = Miner(5000)
# mc1 = Miner(5010)

# mc0.mine_block()

# TODO: For 2 miners
    # TODO: Create and Discover nodes. Check if first node goes to correct if condition
    # TODO: Receive transactions
    # 

# TODO: For 2 separate Client scripts (real thing!)
    # TODO: Mine block concurrently
