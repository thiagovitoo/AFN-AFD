from readFile import read_file

from collections import defaultdict
from itertools import chain, combinations

file_path = 'AFN.txt'
states, alphabet, initial_state, final_states, transitions = read_file(file_path)

print('Estados:', states)
print('Alfabeto:', alphabet)
print('Estado Inicial:', initial_state)
print('Estados Finais:', final_states)
print('Transições:', transitions)


class AFN:
    def __init__(self, estados, alfabeto, transicoes, estado_inicial, estados_finais):
        self.estados = estados
        self.alfabeto = alfabeto
        self.transicoes = transicoes  # dicionário {(estado, símbolo): {conjunto de estados}}
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
        self.transicoes = transicoes  # dicionário {(estado, símbolo): estado}
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

def conversao_powerset(afn):
    # Inicializar o estado inicial do AFD (conjunto contendo o estado inicial do AFN)
    estado_inicial_afd = frozenset([afn.estado_inicial])
    
    # Inicializar estruturas de dados para o AFD
    estados_afd = set()  # Conjuntos de estados do AFD
    transicoes_afd = {}  # Transições do AFD
    estados_finais_afd = set()  # Estados finais do AFD
    estados_nao_marcados = [estado_inicial_afd]  # Estados a serem processados
    
    # Mapear conjuntos de estados do AFN para novos estados do AFD
    while estados_nao_marcados:
        estado_atual_afd = estados_nao_marcados.pop()
        estados_afd.add(estado_atual_afd)
        
        # Verificar se esse conjunto contém algum estado final do AFN
        if any(estado in afn.estados_finais for estado in estado_atual_afd):
            estados_finais_afd.add(estado_atual_afd)
        
        # Para cada símbolo do alfabeto, calcular o novo conjunto de estados
        for simbolo in afn.alfabeto:
            proximo_estado_afd = frozenset(afn.obter_proximos_estados(estado_atual_afd, simbolo))
            
            if proximo_estado_afd:
                # Adicionar a transição para o AFD
                transicoes_afd[(estado_atual_afd, simbolo)] = proximo_estado_afd
                
                # Se esse conjunto ainda não foi processado, adicioná-lo à lista de estados não marcados
                if proximo_estado_afd not in estados_afd and proximo_estado_afd not in estados_nao_marcados:
                    estados_nao_marcados.append(proximo_estado_afd)
    
    # Retornar o AFD construído
    return AFD(estados_afd, afn.alfabeto, transicoes_afd, estado_inicial_afd, estados_finais_afd)

def carregar_afn(caminho_arquivo):
    with open(caminho_arquivo, 'r') as arquivo:
        linhas = arquivo.readlines()
        
        # Exemplo de parsing do arquivo para extrair os estados, alfabeto, transições, etc.
        afn_definicao = linhas[0].strip().split("=")[1].strip("()").split(",")
        estados = set(afn_definicao[0].strip("{}").split(","))
        alfabeto = set(afn_definicao[1].strip("{}").split(","))
        estado_inicial = afn_definicao[2]
        estados_finais = set(afn_definicao[3].strip("{}").split(","))
        
        transicoes = {}
        for linha in linhas[2:]:
            linha = linha.strip()
            if linha:
                partes = linha.split("->")
                estado_simbolo = partes[0].strip().strip("()").split(",")
                estados_destino = set(partes[1].strip().strip("{}").split(","))
                transicoes[(estado_simbolo[0], estado_simbolo[1])] = estados_destino
        
        return AFN(estados, alfabeto, transicoes, estado_inicial, estados_finais)

def carregar_palavras(caminho_arquivo):
    # Carregar palavras do arquivo e retornar como uma lista
    with open(caminho_arquivo, 'r') as arquivo:
        conteudo = arquivo.read().strip()
        palavras = conteudo.split(',')
        return palavras

def verificar_palavras(afd, palavras):
    # Verificar quais palavras são aceitas pelo AFD
    palavras_aceitas = []
    palavras_rejeitadas = []
    
    for palavra in palavras:
        if afd.aceita(palavra):
            palavras_aceitas.append(palavra)
        else:
            palavras_rejeitadas.append(palavra)
    
    return palavras_aceitas, palavras_rejeitadas

# Carregar o AFN do arquivo gerado
afn = carregar_afn("afn_input.txt")

# Converter o AFN para um AFD usando o algoritmo de powerset
afd = conversao_powerset(afn)

# Carregar a lista de palavras do arquivo gerado
palavras = carregar_palavras("palavras.txt")

# Verificar quais palavras são aceitas pelo AFD
palavras_aceitas, palavras_rejeitadas = verificar_palavras(afd, palavras)

# Imprimir as palavras aceitas e rejeitadas
print("Palavras Aceitas:", palavras_aceitas)
print("Palavras Rejeitadas:", palavras_rejeitadas)

# Imprimir os estados e transições do AFD
print("Estados do AFD:", afd.estados)
print("Transições do AFD:", afd.transicoes)
print("Estado inicial do AFD:", afd.estado_inicial)
print("Estados finais do AFD:", afd.estados_finais)
