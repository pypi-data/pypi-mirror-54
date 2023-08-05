# secp256k1-hd-utils

Usage:

```
class TronXPrv(Xprv):
    def pkh_hasher(self, public_key):
        prefix = b'\x41'
        hasher = sha3.keccak_256()
        hasher.update(public_key[1:])
        digest = hasher.digest()[-20:]
        return b58encode_check(prefix + digest)
```