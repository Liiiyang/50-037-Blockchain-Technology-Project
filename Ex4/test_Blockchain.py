from blockchain import *
import requests
import pickle

myId = 5000

# bc = Blockchain.new()
# f = open('./{}/blockchain'.format(myId),'wb')
# pickle.dump(bc,f)
# f.close()

# f = requests.get('http://127.0.0.1:{}/read-blockchain'.format(myId))
# myBlockchain = pickle.loads(f.content)
# print(myBlockchain)

f = requests.get('http://127.0.0.1:{}/read-block-header'.format(myId))