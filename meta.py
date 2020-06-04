from pickle import dump, load

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