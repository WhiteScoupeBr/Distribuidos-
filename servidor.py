import Pyro4

#Classe do Servidor
#Visível ao cliente que acessarem
@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class Servidor(object):
    def __init__(self):
        #Inicializa as variáveis
        self.usuario_carona = []
        self.carona = []
        self.notificacao_carona = []

        self.usuario_caroneiro = []
        self.caroneiro = []
        self.notificacao_caroneiro = []

        self.id_noti_desejo_carona = 0 
        self.id_noti_ofereco_carona = 1000

    #Cadastrar o usuário que deseja uma carona
    def cadastrar_usuario_carona(self, item):
        self.usuario_carona.append(item)
        print(self.usuario_carona)

    #Cadastrar o usuário que oferece uma carona
    def cadastrar_usuario_caroneiro(self, item):
        self.usuario_caroneiro.append(item)
        print(self.usuario_caroneiro)

    #Cadastrar uma demanda de carona
    def desejo_carona(self, item):
        self.carona.append(item)
        self.verifica_caroneiro_noti(item)
        print(self.carona)

    #Cadastrar uma oferta de carona 
    def ofereco_carona(self, item):
        self.caroneiro.append(item)
        self.verifica_carona_noti(item)
        print(self.caroneiro)


    #Verifica se a carona cadastrada satisfaz alguma notificação já cadastrada
    def verifica_caroneiro_noti(self,carona):
        for aux_caroneiro_noti in self.notificacao_caroneiro:
            if  carona['origem']== aux_caroneiro_noti['origem'] and carona['destino'] == aux_caroneiro_noti['destino'] and carona['data']== aux_caroneiro_noti['data']:
                self.publish__(aux_caroneiro_noti,carona)


    #Verifica se a oferta de carona cadastrada satisfaz alguma notificação já cadastrada
    def verifica_carona_noti(self,caroneiro):
        for aux_carona_noti in self.notificacao_carona:
            if  caroneiro['origem']== aux_carona_noti['origem'] and caroneiro['destino'] == aux_carona_noti['destino'] and caroneiro['data']== aux_carona_noti['data']:
                self.publish__(aux_carona_noti,caroneiro)



    #Verifica se alguma oferta carona já cadastrada satisfaz a viagem ofertada pelo caroneiro
    def verifica_nova_noti_carona(self,carona):
        for aux_caroneiro in self.caroneiro:
            if  carona['origem']== aux_caroneiro['origem'] and carona['destino'] == aux_caroneiro['destino'] and carona['data']== aux_caroneiro['data']:
                self.publish__(carona,aux_caroneiro)


    #Verifica se alguma carona já cadastrada satisfaz a viagem ofertada pelo caroneiro
    def verifica_nova_noti_caroneiro(self,caroneiro):
        for aux_carona in self.carona:
            if  caroneiro['origem']== aux_carona['origem'] and caroneiro['destino'] == aux_carona['destino'] and caroneiro['data']== aux_carona['data']:
                self.publish__(caroneiro,aux_carona)

                
    #Cadastra uma notificação, retorna o ID
    def notificao_desejo_carona(self,item,callback):
        self.id_noti_desejo_carona += 1
        item['id'] = self.id_noti_desejo_carona
        item['callback'] = callback
        self.notificacao_carona.append(item)
        print(self.notificacao_carona)
        self.verifica_nova_noti_carona(item)
        return self.id_noti_desejo_carona 

    #Cadastra uma notificação, retorna o ID
    def notificao_ofereco_carona(self,item,callback):
        self.id_noti_ofereco_carona += 1
        item['id'] = self.id_noti_ofereco_carona
        item['callback'] = callback
        self.notificacao_caroneiro.append(item)
        print(self.notificacao_caroneiro)
        self.verifica_nova_noti_caroneiro(item)
        return self.id_noti_ofereco_carona 

    
    #remove a viagem da lista de caronas notificadas
    def cancelar_carona(self,id_cancelar):
        for dicts in self.notificacao_carona:
            for key,value in dicts.items():
                if (key == 'id'):
                    if(int(value) == int(id_cancelar)):
                        self.notificacao_carona.remove(dicts)
                        print(self.notificacao_carona)
                        return "Viagem removida!"
        
        print(self.notificacao_carona)
        return "Id não está na Lista"


    #remove a viagem da lista de caroneiros notificados
    def cancelar_caroneiro(self,id_cancelar):
        for dicts in self.notificacao_caroneiro:
            for key,value in dicts.items():
                if (key == 'id'):
                    if(int(value) == int(id_cancelar)):
                        self.notificacao_caroneiro.remove(dicts)
                        print(self.notificacao_caroneiro)
                        return "Viagem removida!"
        
        print(self.notificacao_caroneiro)
        return "Id não está na Lista"


    
    #Envia os dados da carona para o cliente
    def publish_(self,a):
        
        print(a['callback'])
        c = a['callback']
        c.message(a)


    #Envia os dados da carona para o cliente
    def publish__(self,a,b):
        c = a['callback']
        print(b)
        c.message(b)

Pyro4.Daemon.serveSimple({
    Servidor: "example.servidor"
})