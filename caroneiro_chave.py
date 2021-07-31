from Crypto.PublicKey import RSA
from Crypto.Signature.pkcs1_15 import PKCS115_SigScheme
from Crypto.Hash import SHA256
import binascii
import json


def gerar_chaves():
    key = RSA.generate(bits=1024)
    private_key = key.export_key()
    file_out = open("caroneiro_private.pem", "wb")
    file_out.write(private_key)
    file_out.close()
    return key


def gerar_public(key):
    public_key2 = key.publickey()
    public_key = key.publickey().export_key()
    file_out = open("caroneiro_receiver.pem", "wb")
    file_out.write(public_key)
    file_out.close()
    return public_key2

# Sign the message using the PKCS#1 v1.5 signature scheme (RSASP1)
def assinatura(chaves,msg):
    msg = msg.encode()
    hash = SHA256.new(msg)
    assinante = PKCS115_SigScheme(chaves)
    assinatura = assinante.sign(hash)
    file_out = open("caroneiro_assinatura.bin", "wb")
    file_out.write(assinatura)
    file_out.close()
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

""" 
trythis = {'id':1}
trythis = json.dumps(trythis)
print(type(trythis))

chaves = gerar_chaves()
chave_publica = gerar_public(chaves)

chaves = RSA.import_key(open("carona_private.pem").read())
chave_publica = RSA.import_key(open("carona_receiver.pem").read())

assinatura = assinatura(chaves,trythis)

file = open("carona_assinatura.bin", "rb")
data_sign = file.read()
file.close()

print(verifica_assinatura(chave_publica,data_sign,trythis))
trythis = json.loads(trythis) 
print(type(trythis))
print(trythis) """