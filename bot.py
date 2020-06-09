from pyrogram import Client, MessageHandler, Filters, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
import meta, inspect, logging
import ficha


app = Client("3d&tbot")
player = {}
personagem = {}

logging.basicConfig(level=logging.INFO)

#Classe Criar Personagem. É utilizada pelo bot para receber e armazenar os inputs do usuário necessários
# para criar um nome personagem.
class CriarPersonagem:
    def __init__(self, user):
        self.state = 0
        self.user = user
        self.nome = 'null'
        self.level = 0
        self.raça = 0
    
    def definir_nome(self, nome):
        self.nome = nome
    
    def definir_level(self, level):
        self.level = level
    
    @staticmethod
    def teclado_level():
        teclas = []
        for n in range(1,6):
            teclas.append([KeyboardButton(str(n))])
        print(teclas)
        return ReplyKeyboardMarkup(teclas)
    
    def definir_raça(self, raça):
        self.raça = raça

    @staticmethod
    def teclado_raça():
        teclas = []
        for n in range(1,11):
            raça = ficha.nome_raca(n)
            teclas.append([KeyboardButton(f'{n}.{raça}')])
        print(teclas)
        return ReplyKeyboardMarkup(teclas)

    @staticmethod
    def teclado_s_n():
        teclas = [['Sim', 'Não']]
        return ReplyKeyboardMarkup(teclas)

    def finalizar(self):
        return ficha.criar(self.nome, self.level, self.raça, [], [])

#Recebe o comando "/criar" e inicia o processo de criação do personagem
@app.on_message(Filters.command("criar"))
def criar(client, message):
    chat = message.chat['id']
    app.send_message(chat, 'Oba, vamos criar um personagem novo.\nQual vai ser o nome do seu personagem?')
    player[chat] = CriarPersonagem(chat)
    player[chat].state += 1
    logging.info(f'Criando personagem para o chat:{player[chat].user}. Estado atual: {player[chat].state}')

#Recebe os dados enviados pelo usuário e cria personagem com os dados recebidos 
@app.on_message()
def criar_personagem(client, message):
    try:
        chat = message.chat['id']
        state = player[chat].state
        logging.info(f'Configurando personagem para o chat:{player[chat].user}. Estado atual: {player[chat].state}')
        if state == 1 and chat == player[chat].user:
            player[chat].definir_nome(message.text) 
            app.send_message(chat, 'Lindo nome.\nE qual o level?', reply_markup=CriarPersonagem.teclado_level())
            player[chat].state += 1
            logging.info(f'Definindo nome:{player[chat].nome} para o personagem do chat:{player[chat].user}. Estado atual: {player[chat].state}')
        elif state == 2:
            player[chat].definir_level(int(message.text))
            app.send_message(chat, 'Beleza.\nE qual a raça?', reply_markup=CriarPersonagem.teclado_raça())
            player[chat].state += 1
            logging.info(f'Definindo level:{player[chat].level} para o personagem do chat:{player[chat].user}. Estado atual: {player[chat].state}')
        elif state == 3:
            raça = message.text.split('.')
            raça = int(raça[0])
            player[chat].definir_raça(raça)
            logging.info(f'Definindo raça:{player[chat].raça} para o personagem do chat:{player[chat].user}. Estado atual: {player[chat].state}')
            app.send_message(chat, 'Tudo pronto', reply_markup=ReplyKeyboardRemove())
            player[chat].state += 1
            personagem[chat] = player[chat].finalizar()
            logging.info(f'Finalizando personagem do chat {player[chat]}')
            info = personagem[chat].dados()
            app.send_message(chat, inspect.cleandoc(f"""
            Nome: {info['básico']['Nome']}
            Level: {info['básico']['Nível']}
            Raça: {info['básico']['raca']}
            Atributos:
            Força - {info['atributos']['Força']}
            Habilidade - {info['atributos']['Habilidade']}
            Resistência - {info['atributos']['Resistência']}
            Armadura - {info['atributos']['Armadura']}
            Poder de Fogo - {info['atributos']['Poder de Fogo']}
            Características: {info['características']}
            """))
            app.send_message(chat, 'Deseja salvar esse personagem?', reply_markup=CriarPersonagem.teclado_s_n())
        elif state == 4:
            if message.text == 'Sim':
                stock = ficha.StockPersonagem(chat)
                stock.incluir_personagem(personagem[chat])
                meta.save_obj(stock)
                app.send_message(chat, 'Personagem Salvo', reply_markup=ReplyKeyboardRemove())
            else:
                personagem.pop(chat)
                app.send_message(chat, 'Personagem Apagado', reply_markup=ReplyKeyboardRemove())
    except:
        pass

#Imprime no log as mensagens recebidas para fim de debug
@app.on_message(group = 1)
def imprimir(client, message):
    logging.info(f'Mensagem recebida: {message.text}')

app.run()