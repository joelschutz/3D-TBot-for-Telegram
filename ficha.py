import logging



#Classe Personagem
class Personagem:
    def __init__(self, nome, level=0, raca=0):
        ##Variáveis GLobais

        #Dados do Personagem
        self.nome = nome
    

        #Atributos do Personagem
        # Contem os atributos nessa ordem:
        # 0 - forca, 1 - habilidade, 2 - resistência, 3 - armadura, 4 - Poder de Fogo
        self.atributos = [0,0,0,0,0]
        

        #Pontos de Vida e Magia do personagem, a variante "base" diz respeito aos pontos absolutos
        # antes de qualquer dano ou habilidade ser utilizada.
        self.pontos_vida_base = 0
        self.pontos_vida = 0
        self.pontos_magia_base = 0
        self.pontos_magia = 0


        #Características do Personagem
        self.características = []
        self.tipo_dano = []
        self.magias = []
        self.inventário = []
        self.dinheiro = 0
        self.historia = ''

        #Dados Reservados
        self.pontos = 0
        self.level = level
        self.raca = raca
        
    
    #Getter Level
    @property
    def level(self):
        return self._level

    #Atribui nível ao jogador
    @level.setter
    def level(self, level):
        referencia = [4, 5, 7, 10, 12]
        self.pontos = referencia[int(level)-1]
        self._level = int(level)
        logging.info(f'Level e Pontos atribuidos. Resultado: level={self.level}, pontos={self.pontos}')

    #Getter Pontos
    @property
    def pontos(self):
        return self._pontos

    #Testa se há pontos suficentes para serem gastos
    @pontos.setter
    def pontos(self, pontos):
        if pontos < 0:
            raise ValueError('Não pode ser menor que zero')
        else:
            self._pontos = pontos

    #Getter raca
    @property
    def raca(self):
        return self._raca

    #Seleciona a raca do jogador, atualiza os pontos e características
    @raca.setter
    def raca(self, raca):
        raca = int(raca)
        if raca == 0:
            self._raca = raca
        elif raca in range(1, 36):
            self._raca = raca
            self.pontos = self.pontos - custo_raca(raca)
            self.características = característica_raca(raca)
            self.aplicar_modificadores(modificador_raca(raca))
        logging.info(f'raca atribuida: {nome_raca(raca)}')

    ##Funções

    #Método retorna string formatada para impressão
    def dados(self, dado='full'):
        #Pode retornar string referente a dados básicos, atributos, características ou todos
        referencia = {
            'básico':{
                'Nome': self.nome,
                'Nível': self.level,
                'raca': nome_raca(self.raca),
                'Pontos de Vida': self.pontos_vida_base,
                'Pontos de Magia': self.pontos_magia_base
            },
            'atributos':{
                'Força': self.atributos[0],
                'Habilidade': self.atributos[1],
                'Resistência': self.atributos[2],
                'Armadura': self.atributos[3],
                'Poder de Fogo': self.atributos[4]
            },
            'características' : self.características
        }
        if dado == 'full':
            logging.info(f'Retornando ficha completa')
            return referencia
        else:
            logging.info(f'Retornando parte da ficha: {dado}')
            return referencia[dado]

    # Incrementa ou decremanta atributos "n" vezes
    def modificar_atributos(self, atributo, n=1, soma=True):
        sellegal = ['f','h','r','a','p']
        sel = atributo.lower()
        if soma:
            self.atributos[sellegal.index(sel)] += n
            logging.info(f'Atributo modificado: {sel} + {n}')
        else:
            self.atributos[sellegal.index(sel)] -= n
            logging.info(f'Atributo modificado: {sel} - {n}')

    #Aplica os modificadores da lista dada em "n"
    def aplicar_modificadores(self, n):
        for i in n:
            if i != '0':
                self.modificar_atributos(i[0],int(i[2]),(i[1]=='+'))
        logging.info(f'Modificadores Aplicados: {str(n)}')

    #Distribui os pontos do personagem. Deve ser entregue uma lista contendo strings relativas 
    # aos atributos a serem alterados. Essas strings strings devem seguir o mesmo padrão
    # dos modificadores. Exemplo: ['H+1', 'R+2']
    def distribuir_pontos(self, atributos: list):
        for item in atributos:
            self.aplicar_modificadores(item)
            self.pontos -= int(item[2])         

    #Permite comprar características utilizando pontos. Deve entregue uma lista contendo integers
    # referentes a cada característica a ser comprada
    def comprar_característica(self, características: list):
        #Autorizar compra
        for sel in características:
            if sel in range(1, 138):
                nome = nome_característica(sel)
                custo = custo_característica(sel)
                if (nome in self.características) and (not multipla_característica(sel)):
                    raise OverflowError('Característica única já existe')
                else:
                    self.características.append(nome)
                    self.pontos -= custo
            else:
                raise ValueError('Essa oção não existe')

    ##Métodos

    #Calcula Pontos de Vida:
    def calcular_pontos_vida(self):
        modificador_temp = self.características.count('Pontos de Vida Extras')
        r = self.atributos[2] + (2*modificador_temp)
        if r == 0:
            self.pontos_vida_base = 1
        else:
            self.pontos_vida_base = r * 5
        self.pontos_vida = self.pontos_vida_base
        logging.info(f'Pontos de Vida Calculados. Resultado: {self.pontos_vida}')

    #Calcula Pontos de Magia:
    def calcular_pontos_magia(self):
        modificador_temp = self.características.count('Pontos de Magia Extras')
        r = self.atributos[2] + (2*modificador_temp)
        if r == 0:
            self.pontos_magia_base = 1
        else:
            self.pontos_magia_base = r * 5
        self.pontos_magia = self.pontos_magia_base
        logging.info(f'Pontos de Magia calculados. Resultado: {self.pontos_magia}')

from meta import acessdata
                
#Cria Personagem
def criar(nome: str, level: int, raca: int, características: list, atributos: list):
    per = Personagem(nome, level, raca)
    per.comprar_característica(características)
    per.distribuir_pontos(atributos)
    per.calcular_pontos_vida()
    per.calcular_pontos_magia()
    logging.info(f'Personagem Criado. Nome:{per.nome}')
    return per

#Retorna o nome da Vantagem ou Desvantagem dada em "n"            
def nome_característica(n): 
    tabela = 'características'
    dado = 'nome'
    logging.info(f'Retornando nome da característica {n}')
    return acessdata(tabela, dado, n)

#Retorna Valor da Vantagem ou Desvantagem dada em "n" 
def custo_característica(n):
    tabela = 'características'
    dado = 'custo'
    logging.info(f'Retornando custo da característica {n}')
    return int(acessdata(tabela, dado, n))

#Retorna se a Vantagem ou Desvantagem dada em "n" pode ser comprada multiplas vezes
def multipla_característica(n):
    tabela = 'características'
    dado = 'multiplas'
    logging.info(f'Retornando se {n} é multipla')
    if  acessdata(tabela, dado, n) == 'True' :
        return True
    else:
        return False

#Retorna o nome da raca dada em "n"
def nome_raca(n):
    tabela = 'racas'
    dado = 'nome'
    logging.info(f'Retornando o nome da raca {n}')
    return acessdata(tabela, dado, n)

#Retorna o custo em pontos da raca dada em "n" 
def custo_raca(n):
    tabela = 'racas'
    dado = 'custo'
    logging.info(f'Retornando o custo da raca {n}')
    return int(acessdata(tabela, dado, n))

#Retorna lista de Vantagens e Desvantagens da raca dada em "n"
def característica_raca(n):
    tabela = 'racas'
    dado = 'Vantagens/Desvantagens'
    car = acessdata(tabela, dado, n)
    car = car.split(';')
    lst = []
    for i in car:
        lst.append(nome_característica(int(i)))
    logging.info(f'Retornando lista de características da raca {n}')
    return lst

#Retorna lista de motificadores da raca dada em "n"
def modificador_raca(n):
    tabela = 'racas'
    dado = 'Modificadores'
    modificador_temp = acessdata(tabela, dado, n)
    modificador_temp = modificador_temp.split(';')
    lst = []
    for i in modificador_temp:
        lst.append(i)
    logging.info(f'Retornando lista de modificadores da raca {n}')
    return lst
