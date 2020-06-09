import pickle
import json
import csv
import logging
import ficha

ref = {ficha.Personagem:'.per', ficha.StockPersonagem:'.sper'}


#Salva Objeto em Arquivo
def save_obj(objeto):
    for classe in ref:
        if isinstance(objeto, classe):
            with open(f'{objeto.nome}{ref[classe]}', 'wb') as arquivo:
                    pickle.dump(objeto, arquivo)

#Carrega Objeto de Arquivo
def load_obj(objeto_nome, objeto_tipo):
    with open(f'{objeto_nome}{ref[objeto_tipo]}', 'rb') as arquivo:
        return pickle.load(arquivo)

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

