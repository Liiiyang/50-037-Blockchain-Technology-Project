import random
from ecdsa import SigningKey, VerifyingKey, NIST192p
from Transaction import *
import requests
from MinerClient import *

# TODO: Bob wants to buy item X from Alice.

# At time=0, 
# Alice generates nonce that Bob must input in his transaction. (cryptographic challenge)
random.seed()
challengeNonce = random.randrange(2**256)

# Bob creates Transaction 
sk = SigningKey.from_pem(open("./{}/sk.pem".format(1)).read())
rcv = 'Alice'
snd = 'Bob'
amt = 1
sk_string = sk.to_string()

myTx = Transaction.new(rcv, snd, amt, sk_string, str(challengeNonce))
myTxJSON = myTx.to_json()

headers = {'Content-type': 'application/json'} 
requests.post('http://127.0.0.1:{}/create-transactions'.format(5000), json=myTxJSON ,headers=headers)

# Alice waits for 6 blocks to be added
# Note: May need to delete blockchain file in folder 5010
m = Miner(5010, 6)
m.mine_block()

# Alice gives item X to Bob
