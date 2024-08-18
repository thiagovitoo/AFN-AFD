
def read_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Extrair a linha do autômato
    string = lines[0].strip()

    # Inicializar variáveis
    estados = []
    alfabeto = []
    estado_inicial = ""
    estados_finais = []

    # Ponteiro para percorrer a string
    i = 0

    # Ignorar 'NOME_AUTÔMATO=({'
    while string[i] != '{':
        i += 1

    letra_temp = ""
    while string[i] != '}':
        if string[i] == ',':
            alfabeto.append(letra_temp)
            letra_temp = ""
        else:
            letra_temp += string[i]
        i += 1
    alfabeto.append(letra_temp)  # Adicionar a última letra
    i += 3  # Ignorar '},{'

    estado_temp = ""
    while string[i] != '}':
        if string[i] == ',':
            estados.append(estado_temp)
            estado_temp = ""
        else:
            estado_temp += string[i]
        i += 1
    estados.append(estado_temp)  # Adicionar o último estado
    i += 2  # Ignorar '},'


    # Pegar o estado inicial
    estado_inicial = ""
    while string[i] != ',':
        estado_inicial += string[i]
        i += 1

    # Ignorar ',{'
    i += 2

    estado_final_temp = ""
    while string[i] != '}':
        if string[i] == ',':
            estados_finais.append(estado_final_temp)
            estado_final_temp = ""
        else:
            estado_final_temp += string[i]
        i += 1
    estados_finais.append(estado_final_temp)  # Adicionar o último estado final
    i += 1  # Ignorar '}'

    
    # Ignorar a string "Prog"
    transicoes = {}
    for line in lines[2:]:
        line = line.strip()
        if line:
            estado, transicao = line.split(')=')
            estado, letra  = estado[1:].split(',')  # Converter 'q1, i' para ['q1', 'i']
            transicoes[estado, letra] = transicao[1:-1].split(',')
    
    return estados, alfabeto, estado_inicial, estados_finais, transicoes


def carregar_palavras(caminho_arquivo):
    # Carregar palavras do arquivo e retornar como uma lista
    with open(caminho_arquivo, 'r') as arquivo:
        conteudo = arquivo.read().strip()
        palavras = conteudo.split(',')
        return palavras


if __name__ == '__main__':
    estados, alfabeto, estado_inicial, estados_finais, transicoes = read_file('Entrada/AFN.txt')

    print("ESTADOS:", estados)
    print("ALFABETO:", alfabeto)
    print("ESTADO_INICIAL:", estado_inicial)
    print("ESTADOS_FINAIS:", estados_finais)
    print("TRANSICOES:", transicoes)

    palavras = carregar_palavras("Entrada/palavras.txt")

'''
    Ponteiro da string ignora AUTÔMATO=({

    Enquanto string != '}'
    Pegar os estados [q0,q1,q2,q3]

    Parou na '}' então:
    Ponteiro da string ignora ',{'

    Enquanto string != '}'
    Pegar as letras do alfabeto [a,b]

    Parou na '}' então:

    Pegar [q0]
    Ponteiro da string ignora ',{'

    Enquanto string != '}'
    Pegar os estados finais [q1,q3]

    Ponteiro da string ignora '})'

'''  