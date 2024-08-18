from readFile import read_file, carregar_palavras
from definitions import AFN, AFD
import sys

def main(file_path):

    try: # Caso o arquivo esteja sendo rodado pelo Code Runner do VSCode, tenta pegar o arquivo no argumento do if __name__ == '__main__' no final do arquivo
        estados, alfabeto, estado_inicial, estados_finais, transicoes = read_file(file_path)

    except FileNotFoundError: # Se o arquivo não for encontrado, pega o arquivo no argumento padrão. Ex: python main.py Entrada/AFN.txt
        file_path = sys.argv[1]
        estados, alfabeto, estado_inicial, estados_finais, transicoes = read_file(file_path)

    # Inicializar o AFN
    afn = AFN(estados, alfabeto, transicoes, estado_inicial, estados_finais)

    # Imprimir os estados e transições do AFN
    print("Estados do AFN:", afn.estados)
    print("Transições do AFN:", afn.transicoes)
    print("Estado inicial do AFN:", afn.estado_inicial)
    print("Estados finais do AFN:", afn.estados_finais)

    # Converter o AFN para um AFD usando o algoritmo de powerset
    estados_afd, alfabeto_afd, transicoes_afd, estado_inicial_afd, estados_finais_afd = afn.conversao_powerset()

    # Inicializar o AFD
    afd = AFD(estados_afd, alfabeto_afd, transicoes_afd, estado_inicial_afd, estados_finais_afd)

    # Carregar a lista de palavras do arquivo gerado
    palavras = carregar_palavras('Entrada/palavras.txt')

    # Retorna quais palavras são aceitadas ou rejeitadas pelo AFD
    palavras_aceitas, palavras_rejeitadas = afd.verificar_palavras(palavras)

    #Imprimir as palavras aceitas e rejeitadas
    print("Palavras Aceitas:", palavras_aceitas)
    print("Palavras Rejeitadas:", palavras_rejeitadas)


    # Imprimir os estados e transições do AFD

    # Converter frozenset para set para impressão
    #estados_convertidos = {tuple(estado) for estado in afd.estados}
    #print("Estados do AFD:", estados_convertidos)
    print("Estados do AFD:", afd.estados)

    print("Transições do AFD:", afd.transicoes)
    print("Estado inicial do AFD:", afd.estado_inicial)

    # Converter frozenset para set para impressão
    #estados_finais_convertidos = {tuple(estado) for estado in afd.estados_finais}
    #print("Estados finais do AFD:", estados_finais_convertidos)
    print("Estados finais do AFD:", afd.estados_finais)

if __name__ == '__main__':
    main('Entrada/AFN.txt')