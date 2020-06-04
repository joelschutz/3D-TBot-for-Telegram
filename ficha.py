
import csv

#Classe Personagem
class personagem:
    def __init__(self):
        ##Variáveis GLobais

        #Dados do Personagem
        self.nome = ""
        self.pontos = 0
        self.level = 0
        self.raca = ''

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

    #Calcula Pontos de Magia:
    def calcular_pontos_magia(self):
        modificador_temp = self.características.count('Pontos de Magia Extras')
        r = self.atributos[2] + (2*modificador_temp)
        if r == 0:
            self.pontos_magia_base = 1
        else:
            self.pontos_magia_base = r * 5
        self.pontos_magia = self.pontos_magia_base

    #Atribui nível ao jogador
    def selecionar_level(self, level):
        referencia = [4, 5, 7, 10, 12]
        self.pontos = referencia[level-1]
        self.level = level

    #Seleciona a raça do jogador, atualiza os pontos e características
    def selecioar_raça(self, raça):
        if raça == 0:
            self.raca = 'Humano'
        elif raça in range(1, 36):
            self.raca = self.nome_raça(raça)
            self.pontos = self.pontos - self.custo_raça(raça)
            self.características = self.característica_raça(raça)
            self.aplicar_modificadores(self.modificador_raça(raça))

    #Método retorna string formatada para impressão
    def dados(self, dado='full'):
        #Pode retornar string referente a dados básicos, atributos, características ou todos
        referencia = {'atributos': f'Seus atributos são:\n[F]orça - {self.atributos[0]}\n[H]abilidade - {self.atributos[1]}\n'+
        f'[R]esistência - {self.atributos[2]}\n[A]rmadura - {self.atributos[3]}\n[P]oder de Fogo - {self.atributos[4]}\n',\
             'básicos':f'Nome: {self.nome}\nNível: {self.level}\nRaça: {self.raca}\n' +
        f'Pontos de Vida: {self.pontos_vida_base}\nPontos de Magia: {self.pontos_magia_base}\n',\
             'características' : f'Características: {self.características}\n'}
        if dado == 'full':
            return referencia['básicos'] + referencia['atributos'] + referencia['características']
        else:
            return referencia[dado]
        
    ##Funções

    # Incrementa ou decremanta atributos "n" vezes
    def modificar_atributos(self, atributo, n=1, soma=True):
        sellegal = ['f','h','r','a','p']
        sel = atributo.lower()
        if soma:
            self.atributos[sellegal.index(sel)] += n
        else:
            self.atributos[sellegal.index(sel)] -= n

    #Aplica os modificadores da lista dada em "n"
    def aplicar_modificadores(self, n):
        for i in n:
            if i != '0':
                self.modificar_atributos(i[0],i[2],(i[1]=='+'))

    #Retorna o nome da Vantagem ou Desvantagem dada em "n"            
    def nome_característica(self, n):
        tabela = 'características'
        dado = 'nome'
        return self.acessdata(tabela, dado, n)

    #Retorna Valor da Vantagem ou Desvantagem dada em "n" 
    def custo_característica(self, n):
        tabela = 'características'
        dado = 'custo'
        return int(self.acessdata(tabela, dado, n))

    #Retorna se a Vantagem ou Desvantagem dada em "n" pode ser comprada multiplas vezes
    def multipla_característica(self, n):
        tabela = 'características'
        dado = 'multiplas'
        if  self.acessdata(tabela, dado, n) == 'True' :
            return True
        else:
            return False

    #Retorna o nome da Raça dada em "n"
    def nome_raça(self, n):
        tabela = 'racas'
        dado = 'nome'
        return self.acessdata(tabela, dado, n)

    #Retorna o custo em pontos da Raça dada em "n" 
    def custo_raça(self, n):
        tabela = 'racas'
        dado = 'custo'
        return int(self.acessdata(tabela, dado, n))

    #Retorna lista de Vantagens e Desvantagens da Raça dada em "n"
    def característica_raça(self, n):
        tabela = 'racas'
        dado = 'Vantagens/Desvantagens'
        car = self.acessdata(tabela, dado, n)
        car = car.split(';')
        lst = []
        for i in car:
            lst.append(self.nome_característica(int(i)))
        return lst

    #Retorna lista de motificadores da Raça dada em "n"
    def modificador_raça(self, n):
        tabela = 'racas'
        dado = 'Modificadores'
        modificador_temp = self.acessdata(tabela, dado, n)
        modificador_temp = modificador_temp.split(';')
        lst = []
        for i in modificador_temp:
            lst.append(i)
        return lst

    #Acessa dados nas tabelas indexadas em "refdados". Onde "tipo_dado" é a tabela indexada,
    #"dado" corresponde a coluna e "item" corresponde a linha na tabela.
    def acessdata(self, tipo_dado, dado, item):
        refdados = {'racas':'racas.csv', 'características':'vantagens e desvantagens.csv'}
        tipo_dado = tipo_dado.lower()
        if tipo_dado in refdados:
            with open(refdados[tipo_dado], encoding="utf8") as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                count1 = 0
                count2 = 0
                col = 0
                for linha in csv_reader:
                    if count1 == 0:
                        for d in linha:
                            if dado.lower() == d.lower():
                                col = count2
                            else:
                                count2 += 1
                    elif count1 == item:
                        return linha[col]
                    
                    count1 += 1
                
#Cria Personagem
def criar(personagem, nome, level, raça):
    personagem.nome = nome
    personagem.selecionar_level(level)
    personagem.selecioar_raça(raça)
    comprar_característica(personagem)
    distribuir_pontos(personagem)
    personagem.calcular_pontos_vida()
    personagem.calcular_pontos_magia()
    print(personagem.dados())

#Distribui os pontos do personagem
def distribuir_pontos(personagem):
    print('Vamos distribuir os pontos.')
    while personagem.pontos > 0:
        print(personagem.dados('atributos'))
        print(f'Lhe restam {personagem.pontos} pontos')
        personagem.modificar_atributos(input('Qual atributo quer evoluir?\n[Primeira Letra] ')) 
        personagem.pontos -= 1         
    else:
        print('Não há mais pontos para distribuir!')

#Permite comprar características utilizando pontos
def comprar_característica(personagem):
    while personagem.pontos > 0:
        print(f'Suas Vantagens e Desvantagens são:\n{personagem.características}')
        sel = input('Qual a Vantagem ou Desvantagem quer comprar?\n'+
        f'Você tem {personagem.pontos} pontos. Mande [e] para encerrar.\n[1-137] ')
        if sel.lower() == 'e':
            print('Compra encerrada!')
            break
        elif int(sel) in range(1, 138):
            a = int(sel)
            nome = personagem.nome_característica(a)
            custo = int(personagem.custo_característica(a))
            print(f'Você selecionou {nome}\nCusto: {custo}')
            c = input('Mande [c] para confirmar. Ou outra letra para voltar.')
            if c.lower() == 'c':
                if (nome in personagem.características) and (not personagem.multipla_característica(a)):
                    print('Você já possui essa Vantagem ou Desvantagem.')
                elif (personagem.pontos - custo) >= 0:
                    print(f'Você comprou {nome}!')
                    personagem.características.append(nome)
                    personagem.pontos = personagem.pontos - custo
                else:
                    print('Você não tem pontos suficientes para comprar esse Vantagem ou Desvantagem.')
        else:
            print('Essa opção não é válida!')
    else:
        print('Não há mais pontos para distribuir!')