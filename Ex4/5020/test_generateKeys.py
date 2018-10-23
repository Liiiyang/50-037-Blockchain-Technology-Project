from ecdsa import SigningKey, VerifyingKey, NIST192p

# Generate keys
sk = SigningKey.generate(curve=NIST192p)
vk = sk.get_verifying_key()
open("sk.pem","wb").write(sk.to_pem())
open("vk.pem","wb").write(vk.to_pem())