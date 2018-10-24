'''
SPV client initialisation - Acquiring proofs and transactions
'''
from SPVClient import *

myid = 5000

client = SPVClient(myid)
print("----Sending Transactions----")
print(client.sendTransaction(5000,"you", "me", 5000,"First Transaction"))
print("----Receiving Transactions and Proof----")
msg = client.receiveTransactionASndProofs(5000, 1, "5000").content
msg = pickle.loads(msg)
print(msg)
print("----Get Block Header----")
msg1 = client.getBlockHeader(5000,0).content
msg1 = pickle.loads(msg1)
print(msg1)


from Transaction import *
import requests
from ecdsa import SigningKey, VerifyingKey, NIST192p
import json

rcv = 'Bob'
snd = '5010'
amt = 100000000                     # Value will be ignored by address_balance 
sk = SigningKey.from_pem(open("./{}/sk.pem".format(1)).read())
sk_string = sk.to_string()

myTx = Transaction.new(rcv, snd, amt, sk_string)
myTxJSON = myTx.to_json()
headers = {'Content-type': 'application/json'} 
requests.post('http://127.0.0.1:{}/create-transactions'.format(5010), json=myTxJSON ,headers=headers)

amt = 1                             # Value will be accepted by address_balance 
myTx = Transaction.new(rcv, snd, amt, sk_string)
myTxJSON = myTx.to_json()
requests.post('http://127.0.0.1:{}/create-transactions'.format(5010), json=myTxJSON ,headers=headers)

m = Miner(5010, 6)
m.mine_block()

