from canoser import Struct, Uint8, bytes_to_int_list
from nacl.signing import VerifyKey
from libra.hasher import gen_hasher, HashValue
from libra.transaction.raw_transaction import RawTransaction


ED25519_PUBLIC_KEY_LENGTH = 32
ED25519_SIGNATURE_LENGTH = 64

class SignedTransaction(Struct):
    _fields = [
        ('raw_txn', RawTransaction),
        ('public_key', [Uint8, ED25519_PUBLIC_KEY_LENGTH]),
        ('signature', [Uint8, ED25519_SIGNATURE_LENGTH])
#        ('transaction_length', Uint64)
    ]

    @classmethod
    def gen_from_raw_txn(cls, raw_tx, sender_account):
        tx_hash = raw_tx.hash()
        signature = sender_account.sign(tx_hash)[:64]
        return SignedTransaction(raw_tx,
                bytes_to_int_list(sender_account.public_key),
                bytes_to_int_list(signature)
            )

    def hash(self):
        shazer = gen_hasher(b"SignedTransaction")
        shazer.update(self.serialize())
        return shazer.digest()

    @classmethod
    def from_proto(cls, proto):
        return cls.deserialize(proto.signed_txn)

    def check_signature(self):
        message = self.raw_txn.hash()
        vkey = VerifyKey(bytes(self.public_key))
        vkey.verify(message, bytes(self.signature))

    @property
    def sender(self):
        return self.raw_txn.sender

    @property
    def sequence_number(self):
        return self.raw_txn.sequence_number

    @property
    def payload(self):
        return self.raw_txn.payload

    @property
    def max_gas_amount(self):
        return self.raw_txn.max_gas_amount

    @property
    def gas_unit_price(self):
        return self.raw_txn.gas_unit_price

    @property
    def expiration_time(self):
        return self.raw_txn.expiration_time
