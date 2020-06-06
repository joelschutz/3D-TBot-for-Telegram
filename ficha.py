import logging
import meta

#Classe Personagem
class personagem:
    def __init__(self, nome, pontos=0, level=0, raça=''):
        ##Variáveis GLobais

        #Dados do Personagem
        self.nome = nome
        self.pontos = pontos
        self.level = level
        self.raça = raça

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
    
    #Getter Level
    @property
    def level(self):
        return self._level

    #Atribui nível ao jogador
    @level.setter
    def level(self, level: int):
        referencia = [4, 5, 7, 10, 12]
        self.pontos = referencia[level-1]
        self._level = level
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

    #Getter Raça
    @property
    def raça(self):
        return self._raça

    #Seleciona a raça do jogador, atualiza os pontos e características
    @raça.setter
    def raça(self, raça):
        if raça == 0:
            self._raça = 'Humano'
        elif raça in range(1, 36):
            self._raça = nome_raça(raça)
            self.pontos = self.pontos - custo_raça(raça)
            self.características = característica_raça(raça)
            self.aplicar_modificadores(modificador_raça(raça))
        logging.info(f'Raça atribuida: {self.raça}')

    ##Funções

    #Método retorna string formatada para impressão
    def dados(self, dado='full'):
        #Pode retornar string referente a dados básicos, atributos, características ou todos
        referencia = {'atributos':\
            'Seus atributos são:\n'+\
            f'[F]orça - {self.atributos[0]}\n'+\
            f'[H]abilidade - {self.atributos[1]}\n'+\
            f'[R]esistência - {self.atributos[2]}\n'+\
            f'[A]rmadura - {self.atributos[3]}\n'+\
            f'[P]oder de Fogo - {self.atributos[4]}\n',
            'básicos':\
            f'Nome: {self.nome}\n'+\
            f'Nível: {self.level}\n'+\
            f'Raça: {self.raça}\n'+\
            f'Pontos de Vida: {self.pontos_vida_base}\n'+\
            f'Pontos de Magia: {self.pontos_magia_base}\n',
            'características' : f'Características: {self.características}\n'}
        if dado == 'full':
            logging.info(f'Retornando ficha completa')
            return referencia['básicos'] + referencia['atributos'] + referencia['características']
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

    #Distribui os pontos do personagem
    def distribuir_pontos(self, atributo, valor=1):
        #Autorizar compra
        valor = int(valor)
        self.modificar_atributos(atributo, valor) 
        self.pontos -= valor         

    #Permite comprar características utilizando pontos
    def comprar_característica(self, característica):
        #Autorizar compra
        sel = int(característica)
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

                
#Cria Personagem
def criar(nome: str, level: int, raça: int):
    per = personagem(nome)
    per.level = level
    per.raça = raça
    # comprar_característica(personagem)
    # distribuir_pontos(personagem)
    per.calcular_pontos_vida()
    per.calcular_pontos_magia()
    logging.info(f'Personagem Criado. Nome:{per.nome}')
    return per



#Retorna o nome da Vantagem ou Desvantagem dada em "n"            
def nome_característica(n): 
    tabela = 'características'
    dado = 'nome'
    logging.info(f'Retornando nome da característica {n}')
    return meta.acessdata(tabela, dado, n)

#Retorna Valor da Vantagem ou Desvantagem dada em "n" 
def custo_característica(n):
    tabela = 'características'
    dado = 'custo'
    logging.info(f'Retornando custo da característica {n}')
    return int(meta.acessdata(tabela, dado, n))

#Retorna se a Vantagem ou Desvantagem dada em "n" pode ser comprada multiplas vezes
def multipla_característica(n):
    tabela = 'características'
    dado = 'multiplas'
    logging.info(f'Retornando se {n} é multipla')
    if  meta.acessdata(tabela, dado, n) == 'True' :
        return True
    else:
        return False

#Retorna o nome da Raça dada em "n"
def nome_raça(n):
    tabela = 'racas'
    dado = 'nome'
    logging.info(f'Retornando o nome da Raça {n}')
    return meta.acessdata(tabela, dado, n)

#Retorna o custo em pontos da Raça dada em "n" 
def custo_raça(n):
    tabela = 'racas'
    dado = 'custo'
    logging.info(f'Retornando o custo da raça {n}')
    return int(meta.acessdata(tabela, dado, n))

#Retorna lista de Vantagens e Desvantagens da Raça dada em "n"
def característica_raça(n):
    tabela = 'racas'
    dado = 'Vantagens/Desvantagens'
    car = meta.acessdata(tabela, dado, n)
    car = car.split(';')
    lst = []
    for i in car:
        lst.append(nome_característica(int(i)))
    logging.info(f'Retornando lista de características da raça {n}')
    return lst

#Retorna lista de motificadores da Raça dada em "n"
def modificador_raça(n):
    tabela = 'racas'
    dado = 'Modificadores'
    modificador_temp = meta.acessdata(tabela, dado, n)
    modificador_temp = modificador_temp.split(';')
    lst = []
    for i in modificador_temp:
        lst.append(i)
    logging.info(f'Retornando lista de modificadores da raça {n}')
    return lst
