from pickle import dump, load
import csv
import logging

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
                    logging.info(f'Retornando o dado {dado}, da tabela {tipo_dado}, do item {item}, com valor {linha[col]}')
                    return linha[col]
                
                count1 += 1