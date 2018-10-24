
from Transaction import *
import requests
from ecdsa import SigningKey, VerifyingKey, NIST192p
import json
from MinerClient import *

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

m = Miner(5010, 10)
m.mine_block()
