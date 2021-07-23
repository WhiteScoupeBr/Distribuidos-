# This is the code that visits the warehouse.
import sys
import Pyro4
import Pyro4.util
from caroneiro import Caroneiro

sys.excepthook = Pyro4.util.excepthook


#Procura o servidor dentro da lista, pelo nome
nameserver = Pyro4.locateNS()
uri = nameserver.lookup("example.servidor")
servidor = Pyro4.Proxy(uri)#conecta no servidor localizado

cliente = Caroneiro()#cria o objeto Carona
cliente.acessar(servidor)#Inicia o Menu