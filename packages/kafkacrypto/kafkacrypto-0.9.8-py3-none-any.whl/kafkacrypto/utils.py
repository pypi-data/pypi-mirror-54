import pysodium
import msgpack
from base64 import b64encode, b64decode
from binascii import unhexlify, hexlify, Error as binasciiError
from time import time
from kafkacrypto.exceptions import KafkaCryptoUtilError

def str_decode(value):
  if value!=None:
    try:
      value = int(value)
    except ValueError as e:
      try:
        value = float(value)
      except ValueError as e:
        if value.lower() == "true":
          value = True 
        elif value.lower() == "false":
          value = False
        elif value.startswith("base64#"):
          try:
            value = b64decode(value[7:].encode('utf-8'),validate=True)
          except binasciiError:
            value = None
  elif default!=None:
    return default
  return value

def str_encode(value):
  if value!=None:
    if isinstance(value,(int,float,bool)):
      value = str(value)
    if not isinstance(value,(str,)):
      value = 'base64#' + b64encode(value).decode('utf-8')
  return value

class PasswordProvisioner(object):
  """The PasswordProvisioner class instantiates three provisioner keys, and uses them
  to sign signing keys of new producers/consumers.

  Alternative versions using, e.g. security keys or similar, can also be written.

  Keyword Arguments:
  password (str): Password from which to derive the provisioning secret keys.

  """
  # Constrained devices cannot use larger numbers than interactive
  _ops = pysodium.crypto_pwhash_scryptsalsa208sha256_OPSLIMIT_INTERACTIVE
  _mem = pysodium.crypto_pwhash_scryptsalsa208sha256_MEMLIMIT_INTERACTIVE

  def __init__(self, password, rot):
    if (isinstance(password,(str,))):
      password = password.encode('utf-8')
    try:
      rot = unhexlify(rot)
    except:
      pass
    self._salt = {}
    self._salt['producer'] = pysodium.crypto_hash_sha256(b'producer' + rot)[0:pysodium.crypto_pwhash_scryptsalsa208sha256_SALTBYTES]
    self._salt['consumer'] = pysodium.crypto_hash_sha256(b'consumer' + rot)[0:pysodium.crypto_pwhash_scryptsalsa208sha256_SALTBYTES]
    self._salt['prodcon'] = pysodium.crypto_hash_sha256(b'prodcon' + rot)[0:pysodium.crypto_pwhash_scryptsalsa208sha256_SALTBYTES]
    self._seed = {}
    self._pk = {}
    self._sk = {}
    print("")
    print("Deriving provisioning keys with:")
    print("  opsl = ", self._ops)
    print("  meml = ", self._mem)
    for key in self._salt.keys():
      print("  salt (", key, ") = ", hexlify(self._salt[key]))
      self._seed[key] = pysodium.crypto_pwhash_scryptsalsa208sha256(pysodium.crypto_sign_SEEDBYTES, password, self._salt[key], opslimit=self._ops, memlimit=self._mem)
      self._pk[key], self._sk[key] = pysodium.crypto_sign_seed_keypair(self._seed[key])
      print("  Signing Public Key (", key, "): ", hexlify(self._pk[key]))
    print("")

class PasswordROT(object):
  """The PasswordROT class instantiates a root of trust keypair.

  Alternative versions using, e.g. security keys or similar, can also be written.

  Keyword Arguments:
  password (str): Password from which to derive the secret key.
  """
  # Constrained devices cannot use larger numbers than interactive
  _ops = pysodium.crypto_pwhash_scryptsalsa208sha256_OPSLIMIT_INTERACTIVE
  _mem = pysodium.crypto_pwhash_scryptsalsa208sha256_MEMLIMIT_INTERACTIVE

  def __init__(self, password):
    if (isinstance(password,(str,))):
      password = password.encode('utf-8')
    self._salt = pysodium.crypto_hash_sha256(b'Root of Trust' + password)[0:pysodium.crypto_pwhash_scryptsalsa208sha256_SALTBYTES]
    print("")
    print("Deriving root key with:")
    print("  opsl = ", self._ops)
    print("  meml = ", self._mem)
    print("  salt = ", hexlify(self._salt))
    self._seed = pysodium.crypto_pwhash_scryptsalsa208sha256(pysodium.crypto_sign_SEEDBYTES, password, self._salt, opslimit=self._ops, memlimit=self._mem)
    self._pk, self._sk = pysodium.crypto_sign_seed_keypair(self._seed)
    print("  Root Public Key: ", hexlify(self._pk))
    print("")
