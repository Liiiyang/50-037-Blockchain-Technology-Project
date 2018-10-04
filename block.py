
import hashlib
import json

class Block:
    
    def __init__(self, merkleRoot, timestamp, prevhash, nonce, transactions=[]):
        self.transactions = transactions
        self.header = {
			"prevHeaderHash": prevhash,
        	"merkleRoot": merkleRoot,
        	"nonce": nonce,
			"timestamp": timestamp		#metadata
        }

    def getHeaderInJSON(self):
        return hashlib.sha256(json.dumps(self.header).encode()).hexdigest()

    @property
    def get_block_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()