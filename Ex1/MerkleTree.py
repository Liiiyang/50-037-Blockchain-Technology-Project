'''
Reference guide:
	https://www.codeproject.com/Articles/1176140/Understanding-Merkle-Trees-Why-use-them-who-uses-t
	https://github.com/cliftonm/MerkleTree/blob/master/MerkleTree.cs
	https://github.com/Tierion/pymerkletools/blob/master/tests/test_merkle_tools.py

Special notes:
The server (as trusted authority) doesn't hold the data, 
but it has to have the Merkle tree, including leaf hashes.
'''
import hashlib

# MerkleNode: Intermediate nodes used for linking other nodes.
class MerkleNode():
	def __init__(self, left=None, right=None, leafHash=None):
		if leafHash is None:
			self.myHash = hashlib.sha256(left.myHash + right.myHash).hexdigest()		# hash digest
		else: 
			self.myHash = leafHash
		self.left = left			# MerkleNode
		self.right = right			# MerkleNode
		self.parent = None			# MerkleNode

# MerkleHashProof: Object containing hash and left-checking.
class MerkleHashProof():
	def __init__(self, order, myHash):
		self.is_left = order	# Type: Binary (True means hash belongs to left of concatenation)
		self.myHash = myHash	# Type: 256-bit hash


class MerkleTree():
	def __init__(self):
		self.nodes = []
		self.root = None
		self.list_of_MerkleHashProofs = []
	def add(self, transaction_list):
		# Add entries to tree
		for i in range(len(transaction_list)):

			t = transaction_list[i]
			h = hashlib.sha256(t).hexdigest()
			m = MerkleNode(None, None, h)
			self.nodes.append(m)
	def build(self, list_of_merkleNodes=None):
        # Build tree computing new root
        #
		# Check if 
		# Check if merkle tree has completed due to recursion
		# Extract last_node if list_of_merkleNodes length is odd
		# for each current_working_list_of_nodes
			# Create new node
			# Set children nodes' parent to new node
		# Append new list_of_parent_merkleNodes with last_node
		# Recurse build

		if list_of_merkleNodes is None:
			list_of_merkleNodes = self.nodes

		N = len(list_of_merkleNodes)

		if N == 1:
			self.root = list_of_merkleNodes[0]
		else:
			odd_node = None
			if N % 2 == 1:
				odd_node = list_of_merkleNodes[-1]
				N -= 1
			
			list_of_parent_merkleNodes = []
			for l, r in zip(list_of_merkleNodes[0:N:2], list_of_merkleNodes[1:N:2]):
				parent_node = MerkleNode(l, r)
				list_of_parent_merkleNodes.append(parent_node)
				l.parent = parent_node
				r.parent = parent_node
			if odd_node is not None:
				list_of_parent_merkleNodes.append(odd_node)
			
			self.build(list_of_parent_merkleNodes)
	
	def _build_list_of_MerkleHashProofs(self, leaf_node):
		# Get parent of leaf_node
		# Set Sibling's hash as MerkleProof
		# Check if parent's left node == current leaf_node
		# Set MerkleProof direction depending on ^
		# Append MerkleProof to array

		if leaf_node.myHash == self.root.myHash:
			return None
		else:
			parent_node = leaf_node.parent
			temp_left = parent_node.left
			if temp_left.myHash == leaf_node.myHash:
				is_left = False
				proof_hash = parent_node.right.myHash
			elif parent_node.right.myHash == leaf_node.myHash:
				is_left = True
				proof_hash = parent_node.left.myHash
			else:
				is_left = None
			m = MerkleHashProof(is_left, proof_hash)
			self.list_of_MerkleHashProofs.append(m)
			# Recurse?
			self._build_list_of_MerkleHashProofs(parent_node)
	
	def get_proof(self, myTransaction):
        # Get membership proof for entry
		#
		# Find and get node respective leaf_node
		# Build list of Merkle Hash Proofs
		hashFirst = hashlib.sha256(myTransaction).hexdigest()
		leaf_node = None

		for ln in self.nodes:
			if ln.myHash == hashFirst:
				leaf_node = ln
		if leaf_node is not None:
			self._build_list_of_MerkleHashProofs(leaf_node)
			return self.list_of_MerkleHashProofs
		else:
			return 'invalid!'
		
	def get_root(self):
        # Return the current root
		res = self.root.myHash
		return res
	def _get_nodes(self):
		return self.nodes

def verify_proof(entry, list_of_mhp, root):
	entry = hashlib.sha256(entry).hexdigest()
	current = entry
	for mhp in list_of_mhp:
		if mhp.is_left:
			current = hashlib.sha256(mhp.myHash+current).hexdigest()
		else:
			current = hashlib.sha256(current + mhp.myHash).hexdigest()
		if current == root:
			return True
		else:
			continue
