'''
Requirement:
Design and implement a `Transaction` class that includes the following fields

- sender (a public key of sender)
- receiver (a public key of receiver)
- amount (transaction amount, an integer >0)
- comment (arbitrary text, can be empty)
- signature (sender's signature protecting the transaction)

(**Note:** this interface, maybe w/o `sign()`, will be useful for other future
classes.)

Test your implementation.
- Do you think it makes sense to add any other fields?
- What checks are you going to include within `validate()` ?
- Do you see any challenges in implementing `sign()` and `verify()`?
'''

from ecdsa import SigningKey, VerifyingKey, NIST192p
import json

from Transaction import *

'''
Create keys
Convert to .pem files
Save externally
'''
# Generate keys
# sk = SigningKey.generate(curve=NIST192p)
# vk = sk.get_verifying_key()
# open("sk.pem","w").write(sk.to_pem())
# open("vk.pem","w").write(vk.to_pem())

# Send

vk = VerifyingKey.from_pem(open("vk.pem").read())
sk = SigningKey.from_pem(open("sk.pem").read())

rcv = 'Bob'
snd = 'Alice'
amt = 1
sk_string = sk.to_string()

print sk_string

myTx = Transaction.new(rcv, snd, amt, sk_string)
print myTx.receiver
print myTx.signature
