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
            estado = estado[1:]
            transicoes[estado] = transicao[1:-1].split(',')

    return {
        "ESTADOS": estados,
        "ALFABETO": alfabeto,
        "ESTADO_INICIAL": estado_inicial,
        "ESTADOS_FINAIS": estados_finais,
        "TRANSICOES": transicoes
    }

if __name__ == '__main__':
    automato = read_file('AFN.txt')
    print("ESTADOS:", automato["ESTADOS"])
    print("ALFABETO:", automato["ALFABETO"])
    print("ESTADO_INICIAL:", automato["ESTADO_INICIAL"])
    print("ESTADOS_FINAIS:", automato["ESTADOS_FINAIS"])
    print("TRANSICOES:", automato["TRANSICOES"])

    
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