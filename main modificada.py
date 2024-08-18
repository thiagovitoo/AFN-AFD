from collections import defaultdict
from itertools import chain, combinations

def read_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    string = lines[0].strip()

    estados = []
    alfabeto = []
    estado_inicial = ""
    estados_finais = []

    i = 0
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
    alfabeto.append(letra_temp)
    i += 3

    estado_temp = ""
    while string[i] != '}':
        if string[i] == ',':
            estados.append(estado_temp)
            estado_temp = ""
        else:
            estado_temp += string[i]
        i += 1
    estados.append(estado_temp)
    i += 2

    estado_inicial = ""
    while string[i] != ',':
        estado_inicial += string[i]
        i += 1

    i += 2

    estado_final_temp = ""
    while string[i] != '}':
        if string[i] == ',':
            estados_finais.append(estado_final_temp)
            estado_final_temp = ""
        else:
            estado_final_temp += string[i]
        i += 1
    estados_finais.append(estado_final_temp)
    i += 1

    transicoes = {}
    for line in lines[2:]:
        line = line.strip()
        if line:
            parte_esquerda, parte_direita = line.split(")=")
            estado, simbolo = parte_esquerda[1:].split(',')
            destinos = parte_direita[1:-1].split(',')
            
            transicoes[(estado, simbolo)] = set(destinos)

    return {
        "ESTADOS": estados,
        "ALFABETO": alfabeto,
        "ESTADO_INICIAL": estado_inicial,
        "ESTADOS_FINAIS": estados_finais,
        "TRANSICOES": transicoes
    }

class AFN:
    def __init__(self, estados, alfabeto, transicoes, estado_inicial, estados_finais):
        self.estados = estados
        self.alfabeto = alfabeto
        self.transicoes = transicoes
        self.estado_inicial = estado_inicial
        self.estados_finais = estados_finais

    def obter_proximos_estados(self, estados_atuais, simbolo):
        proximos_estados = set()
        for estado in estados_atuais:
            proximos_estados.update(self.transicoes.get((estado, simbolo), set()))
        return proximos_estados

class AFD:
    def __init__(self, estados, alfabeto, transicoes, estado_inicial, estados_finais):
        self.estados = estados
        self.alfabeto = alfabeto
        self.transicoes = transicoes
        self.estado_inicial = estado_inicial
        self.estados_finais = estados_finais

    def aceita(self, palavra):
        estado_atual = self.estado_inicial
        for simbolo in palavra:
            if (estado_atual, simbolo) in self.transicoes:
                estado_atual = self.transicoes[(estado_atual, simbolo)]
            else:
                return False
            return estado_atual in self.estados_finais

def conversao_powerset(estados, alfabeto, transicoes, estado_inicial, estados_finais):
    estado_inicial_afd = frozenset([estado_inicial])

    estados_afd = set()
    transicoes_afd = {}
    estados_finais_afd = set()
    estados_nao_marcados = [estado_inicial_afd]

    while estados_nao_marcados:
        estado_atual_afd = estados_nao_marcados.pop()
        estados_afd.add(estado_atual_afd)

        if any(estado in estados_finais for estado in estado_atual_afd):
            estados_finais_afd.add(estado_atual_afd)

        for simbolo in alfabeto:
            proximos_estados = set()
            for estado in estado_atual_afd:
                proximos_estados.update(transicoes.get((estado, simbolo), set()))

            proximo_estado_afd = frozenset(proximos_estados)

            if proximo_estado_afd:
                transicoes_afd[(estado_atual_afd, simbolo)] = proximo_estado_afd

                if proximo_estado_afd not in estados_afd and proximo_estado_afd not in estados_nao_marcados:
                    estados_nao_marcados.append(proximo_estado_afd)

    return AFD(estados_afd, alfabeto, transicoes_afd, estado_inicial_afd, estados_finais_afd)

def carregar_palavras(caminho_arquivo):
    with open(caminho_arquivo, 'r') as arquivo:
        conteudo = arquivo.read().strip()
        palavras = conteudo.split(',')
        return palavras

def verificar_palavras(afd, palavras):
    palavras_aceitas = []
    palavras_rejeitadas = []

    for palavra in palavras:
        if afd.aceita(palavra):
            palavras_aceitas.append(palavra)
        else:
            palavras_rejeitadas.append(palavra)

    return palavras_aceitas, palavras_rejeitadas

if __name__ == "__main__":

    # Ler os dados do AFN do arquivo
    dados_afn = read_file('Entrada/AFN.txt')

    # Criação de uma instância de AFN
    afn_instancia = AFN(
        dados_afn["ESTADOS"],
        dados_afn["ALFABETO"],
        dados_afn["TRANSICOES"],
        dados_afn["ESTADO_INICIAL"],
        dados_afn["ESTADOS_FINAIS"]
    )

    # Converter o AFN para AFD
    afd_para_afn = conversao_powerset(
        afn_instancia.estados,
        afn_instancia.alfabeto,
        afn_instancia.transicoes,
        afn_instancia.estado_inicial,
        afn_instancia.estados_finais
    )

    # Carregar a lista de palavras a serem verificadas
    palavras = carregar_palavras("Entrada/palavras.txt")

    # Verificar quais palavras são aceitas pelo AFD
    palavras_aceitas = verificar_palavras(afd_para_afn, palavras)

    # Imprimir as palavras aceitas e rejeitadasprint("Palavras Aceitas:", palavras_aceitas)
    print("Palavras Aceitas:", palavras_aceitas)

    def format_state(state):
        return','.join(state) if isinstance(state, frozenset) else state

    def format_transitions(transitions):
        formatted_transitions = {}
        for (state, symbol), next_state in transitions.items():
            formatted_transitions[(format_state(state), symbol)] = format_state(next_state)
        return formatted_transitions

    # Print the formatted states and transitionsprint("Estados do AFD:", [format_state(state) for state in afd_convertido.estados])
    print("Transições do AFD:", format_transitions(afd_para_afn.transicoes))
    print("Estado inicial do AFD:", format_state(afd_para_afn.estado_inicial))
    print("Estados finais do AFD:", [format_state(state) for state in afd_para_afn.estados_finais])


