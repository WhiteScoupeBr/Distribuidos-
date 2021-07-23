from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64


def gerar_chaves():
    largura_mod = 1024

    chave = RSA.generate(largura_mod)
    # print(chave.exportKey())

    chave_pub = chave.publickey()
    # print(chave_pub.exportKey())

    return chave, chave_pub


def criptografar_chave_privada(msg, chave_priv):
    criptografador = PKCS1_OAEP.new(chave_priv)
    msg_criptografada = criptografador.encrypt(msg)
    #print(msg_criptografada)
    msg_criptografada_codificada = base64.b64encode(msg_criptografada)
    #print(msg_criptografada_codificada)
    return msg_criptografada_codificada


def descriptografar_chave_publica(msg_criptografada_cod, chave_pub):
    criptografador = PKCS1_OAEP.new(chave_pub)
    msg_criptografada_decodificada = base64.b64decode(msg_criptografada_cod)
    #print(msg_criptografada_decodificada)
    msg_descriptografada_decodificada = criptografador.decrypt(
        msg_criptografada_decodificada)
    #print(msg_descriptografada_decodificada)
    return msg_descriptografada_decodificada


def main():
    """ privada, publica = gerar_chaves()
    print(privada)
    mensagem = b'Hello world'
    criptografada = criptografar_chave_privada(mensagem, publica)
    descriptografar_chave_publica(criptografada, privada) """


if __name__ == "__main__":
    main()