from pickle import dump, load
import csv

ref = {'personagem':'.per','mapa':'.map'}

#Salva Objeto em Arquivo
def save_obj(p):
    ps = str(type(p))
    ps = ps.replace("class ", "")
    ps = ps.strip("<>'")
    ps = ps.split('.')
    for i in ps:
        if i in ref:
            with open(f'{p.nome}{ref[i]}', 'wb') as arquivo:
                dump(p, arquivo)

#Carrega Objeto de Arquivo
def load_obj(p, t):
    with open(f'{p}{ref[t]}', 'rb') as arquivo:
                return load(arquivo)

#Acessa dados nas tabelas indexadas em "refdados". Onde "tipo_dado" é a tabela indexada,
#"dado" corresponde a coluna e "item" corresponde a linha na tabela.
def acessdata(tipo_dado, dado, item):
    refdados = {'races':'races.csv', 
                'skills':'skills.csv', 
                'professions':'professions.csv'}
    tipo_dado = tipo_dado.lower()
    if item > 0:
        with open(refdados[tipo_dado], encoding="utf8") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            col = 0
            for count1, linha in enumerate(csv_reader):
                if count1 == 0:
                    for count2, d in enumerate(linha):
                        if dado.lower() == d.lower():
                            col = count2
                elif count1 == item:
                    return linha[col]
    else:
        raise IndexError('Item out of range')

def parse_modifiers(modifiers):
    list = modifiers.split(';')
    MODREF = {
        'S':'Strength',
        'D':'Dexterity',
        'R':'Resistence',
        'I':'Intelligence',
        'A':'Agility',
        'C':'Charisma'}
    if list[0] == '0':
        return {'':None}
    else:
        dic = {}
        for mod in list:
            dic[MODREF[mod[0]]] = int(mod[1:3])
        return dic
