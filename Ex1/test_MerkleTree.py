'''
Reference: 
	https://github.com/cliftonm/MerkleTree/blob/master/MerkleTests/NodeTests.cs

Requirement:
Populate the tree with a random number (between 100-1000) of random transactions, 
compute a root, get proofs for 10 random entries and verify them.

Iterate 100 loops
Instantiate 100 random transactions
Append random transactions into list
Do add()
Do build()
Do get_root(), Do get_proof()
Do verify_proof()
'''

from MerkleTree import *
import hashlib
import json

'''
Create transaction. 
Convert to JSON.
Save externally
'''

# testInput_list = []
# for i in range(100):
# 	msg = str(i)
# 	testInput = hashlib.sha256(msg).hexdigest()
# 	# testInput = testInput.decode('base64','strict')
# 	testInput_list.append(testInput)
# mystr = json.dumps(testInput_list)
# with open('transaction_hash.json', 'w') as outfile:
# 	json.dump(mystr, outfile)

# 

'''
Open JSON
'''

with open('transaction_hash.json') as f:
	data = json.load(f)
data = data.split(",")
data = ['abc','def']

'''
Run test
'''

any_leaf = data[1]

m = MerkleTree()
m.add(data)
m.build()
root = m.get_root()
node = m._get_nodes()
# print 'root is: ' + root
print('root is: {}'.format(root))
proof = m.get_proof(any_leaf)
if proof == False:
	# print 'try again!'
  print('Try again!')
else:
	result = verify_proof(any_leaf, proof, root)
	assert result == True
	# print 'Result is: ' + str(result)
