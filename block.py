import hashlib

class Block:
    
    def __init__(self, root, timestamp, prevhash, transactions):
        self.root = root
        self.nonce = 0
        self.prevhash = prevhash
        self.transactions = transactions
        self.timestamp = timestamp

    @property
    def get_block_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()