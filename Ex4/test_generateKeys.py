from ecdsa import SigningKey, VerifyingKey, NIST192p

# Generate keys
sk = SigningKey.generate(curve=NIST192p)
vk = sk.get_verifying_key()
open("sk_5010.pem","wb").write(sk.to_pem())
open("vk_5010.pem","wb").write(vk.to_pem())