from Crypto.PublicKey import RSA
from Crypto.Signature.pkcs1_15 import PKCS115_SigScheme
from Crypto.Hash import SHA256
import binascii

# Generate 1024-bit RSA key pair (private + public key)

def gerar_chaves():
    return RSA.generate(bits=1024)


def gerar_public(chaves):
    return chaves.publickey()

# Sign the message using the PKCS#1 v1.5 signature scheme (RSASP1)
def assinatura(chaves,msg):
    msg = msg.encode()
    hash = SHA256.new(msg)
    assinante = PKCS115_SigScheme(chaves)
    assinatura = assinante.sign(hash)
    return assinatura

# Verify valid PKCS#1 v1.5 signature (RSAVP1)
def verifica_assinatura(chave_publica,assinatura,msg):
    msg = msg.encode()
    hash = SHA256.new(msg)
    verifier = PKCS115_SigScheme(chave_publica)
    try:
        verifier.verify(hash, assinatura)
        return True
    except:
        return False

# Verify invalid PKCS#1 v1.5 signature (RSAVP1)


#haves = gerar_chaves()
#chave_publica = gerar_public(chaves)
#assinatura = assinatura(chaves,'Hello World')
#print(verifica_assinatura(chave_publica,assinatura,'Hello World'))