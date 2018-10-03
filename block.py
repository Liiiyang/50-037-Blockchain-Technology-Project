import hashlib

class Block:
    
    def __init__(self, merkleRoot, timestamp, prevhash, transactions):
        self.prevHeaderHash = prevHeaderHash
        self.transactions = transactions		
        self.timestamp = timestamp		#metadata
        self.header = {
        	"root": root,
        	"merkleRoot": merkleRoot,
        	"nonce": hashlib.sha256(random.random()).hexdigest()

        }

    @property
    def get_block_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()