import hashlib
import json
from MerkleTree import *

class Block:
    
    def __init__(self, timestamp, prevhash, nonce, transactions):
        self.transactions = transactions
        # Initialize MerkleTree
        self._myMerkle = MerkleTree()
        self._myMerkle.add(transactions)
        self._myMerkle.build()
        _merkleRoot = self._myMerkle.get_root()

        self.header = {
			"prevHeaderHash": prevhash,
        	"merkleRoot": _merkleRoot,
        	"nonce": nonce,
			"timestamp": timestamp		#metadata
        }
    
    # @classmethod
    # def new(self, timestamp, prevHash, nonce, transactions):
    #     pass

    # def to_json(self):
    #     # Serializes object to JSON string
    #     return json.dumps(self.__dict__)

    # @classmethod
    # def from_json(cls, jsonString):
    #     # Instantiates/Deserializes object from JSON string
    #     x = json.loads(jsonString, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
    #     return x

    def get_merkleProofs(self, myTransaction):
        return self._myMerkle.get_proof(myTransaction)

    def getHeaderInHash(self):
        return hashlib.sha256(json.dumps(self.header).encode()).hexdigest()
    # @property
    # def get_block_hash(self):
    #     block_string = json.dumps(self.__dict__, sort_keys=True)
    #     return hashlib.sha256(block_string.encode()).hexdigest()