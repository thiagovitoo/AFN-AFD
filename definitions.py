
class AFN:
    def __init__(self, estados, alfabeto, transicoes, estado_inicial, estados_finais):
        self.estados = estados
        self.alfabeto = alfabeto
        self.transicoes = transicoes  # dicionário {(estado, símbolo): {conjunto de estados}}
        self.estado_inicial = estado_inicial
        self.estados_finais = estados_finais

    def conversao_powerset1(self):
        # Inicialização
        fila = [self.estado_inicial]
        afd_estados = { self.estado_inicial }
        afd_transicoes = self.transicoes

        # Enquanto houver estados a processar
        while fila:
            current = fila.pop(0)
            
            # Para cada símbolo no alfabeto
            for A in self.alfabeto:
                next = set()
                
                # Para cada estado em 'current', adicione os estados alcançáveis com A a 'next'
                for estado in current:
                    chave = f'{estado},{A}'
                    if chave in self.transicoes:
                        next.update(self.transicoes[chave])  # adicione todos os estados alcançáveis
                                
                if next:  # Somente adiciona se houver estados alcançáveis
                    next = frozenset(next)  # Para garantir que seja imutável e possa ser usado como chave
                    
                    # Se 'next' é um novo estado, adicione-o ao AFD
                    if next not in afd_estados:
                        afd_estados.add(next)
                        fila.append(next)
                    
                    # Adicione a transição ao AFD
                    afd_transicoes[(tuple(current), A)] = tuple(next)

        # Determinar os estados finais do AFD
        afd_finais = {estado for estado in afd_estados if any(q in self.estados_finais for q in estado)}

        return afd_estados, self.alfabeto, afd_transicoes, {self.estado_inicial}, afd_finais
    
    def conversao_powerset(self):
        # Inicialização
        afd_estados = {self.estado_inicial}
        afd_transicoes = {}

        # Construção das transições e estados do AFD
        for (estado_origem, simbolo), estados_destino in self.transicoes.items():
            # Verificar se estado_origem é uma lista, se não for, converter para lista
            if not isinstance(estado_origem, list):
                estado_origem = [estado_origem]
            
            afd_transicoes = set()
            
            for estado_destino in estados_destino:
                estado_acumulado = estado_origem + [estado_destino]
                nova_transicao = (tuple(estado_acumulado), simbolo)
                afd_transicoes.add(nova_transicao)
                afd_estados.add(estado_destino)

        # Determinar os estados finais do AFD
        afd_finais = {estado for estado in afd_estados if any(q in self.estados_finais for q in estado)}

        # Itera sobre cada estado no conjunto de estados do AFD
        for estado in afd_estados:
            # Verifica se algum dos estados do AFN que compõem o estado do AFD é um estado final do AFN
            if any(q in self.estados_finais for q in estado):
                # Se for, adiciona o estado do AFD ao conjunto de estados finais do AFD
                afd_finais.add(estado)

        return afd_estados, self.alfabeto, afd_transicoes, {self.estado_inicial}, afd_finais

class AFD:
    def __init__(self, estados, alfabeto, transicoes, estado_inicial, estados_finais):
        self.estados = estados
        self.alfabeto = alfabeto
        self.transicoes = transicoes  # dicionário {(estado, símbolo): estado}
        self.estado_inicial = estado_inicial
        self.estados_finais = estados_finais

    def aceita(self, palavra):
        # Supondo que `estado_atual` seja um conjunto (set), converta-o para frozenset
        estado_atual_frozenset = frozenset(self.estado_inicial)
        
        # Use o frozenset como chave no dicionário de transições
        if (estado_atual_frozenset, palavra) in self.transicoes:
            # Acesse a transição usando o frozenset
            estado_atual_frozenset = self.transicoes[(estado_atual_frozenset, palavra)]
        else:
            return False
        return True

    def verificar_palavras(self, palavras):
        # Verificar quais palavras são aceitas pelo AFD
        palavras_aceitas = []
        palavras_rejeitadas = []
        
        for palavra in palavras:
            if self.aceita(palavra): # Se a palavra é aceita pelo AFD
                palavras_aceitas.append(palavra) # Adiciona a palavra na lista de palavras aceitas
            else:
                palavras_rejeitadas.append(palavra) # Se não, adiciona na lista de palavras rejeitadas
        
        return palavras_aceitas, palavras_rejeitadas
