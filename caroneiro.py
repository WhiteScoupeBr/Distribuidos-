import sys
import threading
import Pyro4


if sys.version_info < (3, 0):
    input = raw_input


# The daemon is running in its own thread, to be able to deal with server
# callback messages while the main thread is processing user input.

class Caroneiro(object):
    def __init__(self):
        self.servidor = Pyro4.core.Proxy('PYRONAME:example.servidor')
        self.abort = 0


    @Pyro4.expose
    @Pyro4.oneway
    def message(self, msg):
        print("NOVA NOTIFICAÇÃO:")
        print("Dados da Carona")
        print(msg['nome'])
        print(msg['telefone'])
        print("Dados da viagem")
        print(msg['origem'])
        print(msg['destino'])
        print(msg['data'])


    def start(self):
        
        #self.cadastrar()
        self.inserir_carona()
        while(True):
            option = input("1 - Cancelar Carona \n2 - Acompanhar notificação\n3 - Fazer nova viagem \n0 - Sair\n").strip()
            if(option == '1'):
                self.cancelar_carona()
            elif(option == '2'):
                pass
            elif(option == '3'):
                self.inserir_carona()
            elif(option == '0'):
                break
            else:
                print("Opção Inválida")

        print("Arigato!")

        self.abort = 1
        self._pyroDaemon.shutdown()


    def cadastrar(self):
        nome = input("Insira seu nome: ").strip()
        telefone = input("Insira seu telefone: ").strip()
        if (nome and telefone):
            item = {'nome':nome,'telefone':telefone}
            self.servidor.cadastrar_usuario_carona(item)
            print("Usuário cadastrado com sucesso! \n")
        else:
            print("Faltam dados! \n")
    


    def inserir_carona(self):
        print("Vamos cadastrar sua viagem desejada! \n")
        nome = input("Insira seu nome para a carona: ").strip()
        telefone = input("Insira seu telefone a carona: ").strip()
        origem = input("Insira seu local de origem: ").strip()
        destino = input("Insira seu local de destino: ").strip()
        data = input("Insira a data no formato dd/mm/aaaa: ").strip()
        n_passageiros = input("Insira quantos passageiros você pode levar: ").strip()
        if (origem and destino and data and n_passageiros):
            item = {'nome':nome,'telefone':telefone,'origem':origem,'destino':destino,'data':data, 'n_passageiros':n_passageiros}
            self.servidor.ofereco_carona(item)
        notificacao = input("Deseja receber notificação caso algum passageiro atenda esses critérios? \n s para Sim \n n para Não\n").strip()
        if(notificacao == 's'):
            self.cadastrar_notificacao(item)
        else:
            print('ok :(\n')



    def cadastrar_notificacao(self,viagem):
            print("Cadastrando sua viagem para ser notificada...\n")
            item = {'nome':viagem['nome'],'telefone':viagem['telefone'],'origem':viagem['origem'],'destino':viagem['destino'],'data':viagem['data']}
            id_noti = self.servidor.notificao_ofereco_carona(item,self)
            print("O id da sua viagem é: ")
            print(id_noti)


    
    #Remove a carona por ID
    def cancelar_carona(self, servidor):
        id_cancelar = input("Insira o Id da viagem que deseja cancelar: \n").strip()
        response = self.servidor.cancelar_caroneiro(id_cancelar)
        print(response)

            

class DaemonThread(threading.Thread):
    def __init__(self, caroneiro):
        threading.Thread.__init__(self)
        self.caroneiro = caroneiro
        self.setDaemon(True)

    def run(self):
        with Pyro4.core.Daemon() as daemon:
            daemon.register(self.caroneiro)
            daemon.requestLoop(lambda: not self.caroneiro.abort)


caroneiro = Caroneiro()
daemonthread = DaemonThread(caroneiro)
daemonthread.start()
caroneiro.start()
print('Exit.')