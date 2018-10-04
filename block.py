import hashlib
import json

class Block:
    
    def __init__(self, merkleRoot, timestamp, prevhash, nonce, transactions=[]):
        self.transactions = transactions
        self.header = {
			"prevHeaderHash": prevhash
        	"root": root,
        	"merkleRoot": merkleRoot,
        	"nonce": nonce
			"timestamp": time.time()		#metadata
        }

	def getHeaderInJSON(self):
		return json.dumps(self.header)

    @property
    def get_block_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()