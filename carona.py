from __future__ import print_function
import sys
import signature 

if sys.version_info < (3, 0):
    input = raw_input

#Atributos do Carona
class Carona(object):
    def __init__(self):
        self.nome = ''
        self.telefone = ''
        #implementar 
        self.id_noti = ''

    #loop de menu
    def acessar(self, servidor):
        self.cadastrar(servidor)
        self.inserir_carona(servidor)
        while(True):
            option = input("1 - Cancelar Carona \n2 - Acompanhar notificação\n 3 - Fazer nova viagem \n0 - Sair\n").strip()
            if(option == '1'):
                self.cancelar_carona(servidor)
            elif(option == '2'):
                pass
            elif(option == '3'):
                self.inserir_carona(servidor)
            elif(option == '0'):
                break
            else:
                print("Opção Inválida")
            print("Arigato!")


    #Quando o usuário deseja ser notificado
    def cadastrar_notificacao(self,servidor,viagem):
            print("Cadastrando sua viagem para ser notificada...\n")
            nome = self.nome
            telefone = self.telefone
            item = {'nome':nome,'contato':telefone,'origem':viagem['origem'],'destino':viagem['destino'],'data':viagem['data']}
            self.id_noti = servidor.notificao_desejo_carona(item)
            print("O id da sua viagem é: ")
            print(self.id_noti)


    #cadastra o usuário no sistema
    def cadastrar(self, servidor):
        nome = input("Insira seu nome: ").strip()
        telefone = input("Insira seu telefone: ").strip()
        if (nome and telefone):
            item = {'nome':nome,'telefone':telefone}
            servidor.cadastrar_usuario(item)
            print("Usuário cadastrado com sucesso! \n")
        else:
            print("Faltam dados! \n")


    #Insere na lista de caronas, mas nao ainda na de notificação
    def inserir_carona(self, servidor):
        print("Vamos cadastrar sua viagem desejada! \n")
        origem = input("Insira seu local de origem: ").strip()
        destino = input("Insira seu local de destino: ").strip()
        data = input("Insira a data no formato dd/mm/aaaa: ").strip()
        if (origem and destino and data):
            item = {'origem':origem,'destino':destino,'data':data}
            servidor.desejo_carona(item)
        notificacao = input("Deseja receber notificação caso alguma viagem atenda esses critérios? \n s para Sim \n n para Não\n").strip()
        if(notificacao == 's'):
            self.cadastrar_notificacao(servidor,item)
        else:
            print('ok :(\n')

    #Remove a carona por ID
    def cancelar_carona(self, servidor):
        id_cancelar = input("Insira o Id da viagem que deseja cancelar: \n").strip()
        response = servidor.cancelar_carona(id_cancelar)
        print(response)
    

