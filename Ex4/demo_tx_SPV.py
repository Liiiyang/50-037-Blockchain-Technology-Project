# TODO: (Network) Instantiate Mining
# TODO: 

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
