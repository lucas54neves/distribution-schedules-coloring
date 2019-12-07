'''
Algoritmos em Grafos
GCC218 - 2019/02
Trabalho Final de Algoritmos em Grafos
Grupo:
    Lucas Neves, 14A, 201720357
    Davi Horner, 10A, 201720368
    Thiago Luigi, 10A, 201720364
'''

#!/usr/bin/python
# -*- coding: utf-8 -*-

import xlrd
import time
import math

# Classe que representa os vertices
class Vertice:
    # Construtor da classe
    def __init__(self, indice, materia, professor, turma):
        # Indice do vertice na lista dos vertices
        self.indice = indice
        # Materia da aula
        self.materia = materia
        # Professor que ministra a aula
        self.professor = professor
        # Turma da aula
        self.turma = turma
        # Vertices adjacentes a esse vertice
        self.adjacentes = []
        # As cores como padrao sao atribuidas -1
        self.cor = -1

    # Metodo que adiciona um vertice adjacente
    def adicionar_adjacente(self, adjacente):
        self.adjacentes.append(adjacente)

    # Retorna o grau do vertice
    def get_grau(self):
        return len(self.adjacentes)

    # Retorna o grau de saturacao do vertice
    # A saturacao eh o numero de diferentes cores para qual o vertice eh adjacente
    # Para calcular a saturacao, o metodo percorre todos os vertices adjacentes
    # e incrmenta o valor da saturacao para os vertices adjacentes que ja foram
    # coloridos
    def get_saturacao(self):
        saturacao = 0
        for adjacente in self.adjacentes:
            if adjacente.cor is not -1:
                saturacao += 1
        return saturacao

    # Retorna a menor cor disponivel
    def menor_cor_disponivel(self, horarios, restricoes):
        # A menor cor comeca com zero
        menor = 0
        # Ordena os adjacentes por cor para melhorar a eficiente da busca de cores
        self.adjacentes.sort(key=lambda vertice: vertice.cor)
        # Passa por todos os vertices adjacentes verificando as cores
        for vertice in self.adjacentes:
            if vertice.cor == menor:
                menor += 1
                # Verifica se a cor esta dentro dos horarios disponiveis
                if (menor >= len(horarios)):
                    menor = self.cor_menos_frequente()
        # Retorna a menor cor disponivel
        return menor

    # Metodo que verifica a proxima melhor cor disponivel
    # Diferente do metodo menor_cor_disponivel(self, horarios, restricoes), esse
    # metodo calcula a melhor cor considerando uma cor sendo indisponivel
    def melhor_cor_disponivel(self, horarios):
        # A cor comeca com zero
        proxima = 0
        # Ordena os adjacentes por cor para melhorar a eficiente da busca de cores
        self.adjacentes.sort(key=lambda vertice: vertice.cor)
        # Passa por todos os vertices adjacentes verificando as cores
        for adjacente in self.adjacentes:
            # Se a cor do vertice for igual a cor do vertice adjacente, seleciona
            # a proxima cor
            if proxima == adjacente.cor:
                proxima += 1
                # Se a cor for igual a cor inicial do vertice (cor indisponivel)
                # seleciona a proxima cor
                if proxima == self.cor:
                    proxima += 1
            # Verifica se a cor esta dentro dos horarios disponiveis
            if (proxima >= len(horarios)):
                # Se a cor ultrapassar o limite de cores, a cor menos frequente
                # entre os adjacentes eh escolhida como a proxima cor disponivel
                proxima = self.cor_menos_frequente()
        # Retorna a cor melhor disponivel
        return proxima

    # Metodo que verifica se eh possivel atender a preferencia do professor
    def verificar_preferencia(self, cor):
        # Passa por todos os vertices adjacentes verificando se eh possivel mudar
        # a cor do vertice em questao
        for adjacente in self.adjacentes:
            if adjacente.cor == cor:
                # Retorna falso
                return False
        # Muda a cor
        self.cor = cor
        # Retorna verdadeiro
        return True

    # Metodo que tenta resolver as janelas if math.ceil(vertice1.cor / aulas_por_dia) == math.ceil(vertice2.cor / aulas_por_dia):
    def cor_disponivel_janela(self, vertice_aula_anterior, aulas_por_dia, horarios):
        # A melhor cor comeca com a cor seguinte do vertice da aula anterior
        melhor = vertice_aula_anterior.cor + 1
        # Ordena os vertices adjacentes por cor para melhorar a eficiencia da busca
        self.adjacentes.sort(key=lambda vertice: vertice.cor)
        # Loop que verifica se tem alguma vertice adjacente com a possivel melhor
        # cor
        for adjacente in self.adjacentes:
            # Verifica se existe algum vertice adjacente com a possivel melhor cor
            if melhor == adjacente.cor:
                # Escolhe a proxima cor como a possivel melhor cor
                melhor += 1
            # Verifica se a cor esta dentro dos horarios disponiveis
            if (melhor >= len(horarios)):
                # Se a cor ultrapassar o limite de cores, a cor menos
                # frequente entre os adjacentes eh escolhida como a
                # possivel melhor cor
                melhor = self.cor_menos_frequente()
        # Retorna a melhor cor disponivel para janela
        return melhor

    # Metodo que escolhe a cor menos frequente entre os vertices adjacentes
    # Isso ocorre para limitar a quantidade de cores pelo quantidade de horarios
    def cor_menos_frequente(self):
        # Dicionario para armazenar a frequencia de cores
        frequencia_cores = {}
        # Loop que calcula a frequencia de cores
        for adjacente in self.adjacentes:
            # Verifica se a cor ja se encontra no dicionario. Se ela tiver, eh
            # apenas incrementada
            if adjacente.cor in frequencia_cores:
                frequencia_cores[adjacente.cor] = frequencia_cores.get(adjacente.cor) + 1
            # Caso a cor nao se encontra no dicionario, eh atribuido a ela o
            # valor 1
            else:
                frequencia_cores[adjacente.cor] = 1
        # Retorna a cor o valor menos frequente em relacao aos adjacentes
        return min(frequencia_cores, key = frequencia_cores.get)

# Classe que representa os grafos
class Grafo:
    # Construtor do grafo
    def __init__(self, nome_arquivo, nome_escola):
        # Lista que armazena os vertices do grafo
        self.vertices = []
        # Lista que armazena as horas disponiveis para aula por dia
        self.horas = []
        # Lista que armazena os horarios disponiveis para aula por semana
        self.horarios = []
        # Dicionario que armazena as restricoes de horarios dos professores
        self.restricoes_professores = {}
        # Dicionario que armazena as restricoes de horarios das turmas
        self.restricoes_turmas = {}
        # Dicionario que armazena as preferencias de horarios dos professores
        self.preferencias_professores = {}
        # Dicionario que armazena a quantidade de preferenciais atendidas para
        # cada professor
        self.preferenciais_atendidas = {}
        # Variavel para guardar a quantidade de vertices coloridos
        self.vertices_coloridos = 0
        # Nome da escola para imprimir no resultado
        self.nome_escola = nome_escola
        # Metodo que realiza a leitura do arquivo
        self.ler_arquivo(nome_arquivo)
        # Variavel que para armazenar a quantidade de vertices nao coloridos
        self.quantidade_vertices_nao_coloridos = len(self.vertices)
        # Metodo que verifica todas as restricoes
        self.verificar_restricoes()
        # Tempo inicial
        inicio = time.time()
        # Metodo que colere o grafo
        self.dsatur()
        # Metodo que verifica se as cores (horarios) estao de acordo com as
        # restricoes dos professores
        self.verificar_restricoes_professores()
        # Metodo que verifica se existe tres ou mais aulas geminadas
        self.verificar_geminadas()
        # Metodo que verifica se existe grande janelas de horarios para uma turma
        self.verificar_janelas()
        # Metodo que verifica as preferencias dos professores
        self.verificar_preferencias()
        # Tempo final
        fim = time.time()
        # Variavel que armazena o tempo de execucao do algoritmo
        self.tempo_iteracao = fim - inicio
        # Variavel que armazena a quantidade de cores usadas
        # Como existe a cor zero, a quantidade de cores sera o valor sucessor
        # ao valor relativo a maior cor
        self.quantidade_cores = max(self.vertices, key =  lambda vertice: vertice.cor).cor + 1

    # Metodo para a leitura do arquivo
    def ler_arquivo(self, nome_arquivo):
        # Abertura do arquivo
        planilha = xlrd.open_workbook(nome_arquivo)
        # Leitura da aba Dados da planilha
        self.ler_dados(planilha)
        # Leitura da aba Configuracoes da planilha
        self.ler_configuracoes(planilha)
        # Leitura da aba Restricoes da planilha
        self.ler_restricoes_professores(planilha)
        # Leitura da aba Restricoes Turma da planilha
        self.ler_restricoes_turma(planilha)
        # Leitura da aba preferencias da planilha
        self.ler_preferencias(planilha)

    # Metodo que realiza a leitura da aba Dados da planilha
    def ler_dados(self, planilha):
        # Pega a primeira aba da planilha
        aba = planilha.sheet_by_index(0)
        # Loop para leitura das linhas
        for i in range(aba.nrows):
            if i != 0:
                valores = aba.row_values(i)
                # Pega a letra relativa a materia
                materia = valores[0]
                # Pega o numero relativo a turma
                turma = valores[1]
                # Pega o numero relativo ao professor
                professor = valores[2]
                # Pega a quantidade de aulas
                quantidade_aulas = int(valores[3])
                # Adiciona o vertice com as informacoes coletas nessa linha da aba.
                # Cada aula eh representada por um vertice. Se existe uma materia A
                # que eh ministrada por um professor 1 para uma turma B que possui
                # 3 aulas, 3 vertices seram adicionados para representar cada uma
                # das aulas.
                for i in range(quantidade_aulas):
                    vertice = Vertice(len(self.vertices), materia, professor, turma)
                    self.adicionar_vertice(vertice)

    # Metodo que realiza a leitura da aba Configuracoes da planilha
    def ler_configuracoes(self, planilha):
        # Pega a segunda aba da planilha
        # Nessa aba, estao as horas disponiveis nos dias
        aba = planilha.sheet_by_index(1)
        # Loop para leitura das linhas
        for i in range(aba.nrows):
            if i != 0:
                valores = aba.row_values(i)
                # Pega a hora dessa linha da aba
                hora = float(valores[0])
                # Adiciona a hora a lista de horas
                self.adicionar_hora(hora)
        self.criacao_cores()

    # Metodo que realiza a leitura da aba Restricoes da planilha
    def ler_restricoes_professores(self, planilha):
        # Pega a terceira aba da planilha
        # Essa aba estao as restricoes de horarios de cada professor
        aba = planilha.sheet_by_index(2)
        # Loop para leitura das linhas
        for i in range(aba.nrows):
            if i != 0:
                valores = aba.row_values(i)
                # Pega o numero relativo ao professor
                professor = valores[0]
                # Pega a hora da preferencia de horario
                hora = float(valores[1])
                # Pega o dia da preferencia de horario
                dia = str(valores[2])
                self.adicionar_restricoes_professores(professor, hora, dia)

    # Metodo que realiza a leitura da aba Restricoes Turmas da planilha
    def ler_restricoes_turma(self, planilha):
        # Pega a quarta aba da planilha
        # Nessa aba tem as restricoes de horarios de cada turma
        aba = planilha.sheet_by_index(3)
        # Loop para leitura das linhas
        for i in range(aba.nrows):
            if i != 0:
                valores = aba.row_values(i)
                # Pega o numero relativo a turma
                turma = valores[0]
                # Pega a hora da preferencia de horario
                hora = float(valores[1])
                # Pega o dia da preferencia de horario
                dia = str(valores[2])
                self.adicionar_restricoes_turmas(turma, hora, dia)

    # Metodo que realiza a leitura da aba Preferencias da planilha
    def ler_preferencias(self, planilha):
        # Pega a quinta aba da planilha
        # Essa aba estao as preferencias de horarios de cada professor
        aba = planilha.sheet_by_index(4)
        # Loop para leitura das linhas
        for i in range(aba.nrows):
            if i != 0:
                valores = aba.row_values(i)
                # Pega o numero relativo ao professor
                professor = valores[0]
                # Pega a hora da preferencia de horario
                hora = float(valores[1])
                # Pega o dia da preferencia de horario
                dia = str(valores[2])
                self.adicionar_preferencias_professores(professor, hora, dia)

    # Metodo que adiciona um vertice a lista de vertices
    def adicionar_vertice(self, vertice):
        self.vertices.append(vertice)

    # Metodo que adiciona uma hora a lista de horas
    def adicionar_hora(self, hora):
        self.horas.append(hora)

    # Metodo que cria os horarios (conjunto de hora e dia)
    def criacao_cores(self):
        # Dias disponiveis
        dias = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]
        # Loop que cria os horarios
        for dia in dias:
            for hora in self.horas:
                self.adicionar_horario(hora, dia)

    # Metodo que adiciona um horario a lista de horarios
    def adicionar_horario(self, hora, dia):
        self.horarios.append([hora, dia])

    # Metodo que adiciona uma restricao a lista de restricoes dos professores
    def adicionar_restricoes_professores(self, professor, hora, dia):
        # Se o professor ja tiver uma restricao na lista
        if professor in self.restricoes_professores:
            self.restricoes_professores.get(professor).append([hora, dia])
        # Se o professor nao tiver uma restricao na lista
        else:
            # Cria uma lista para guardar as restricoes
            self.restricoes_professores[professor] = []
            # Adiciona a restricao a lista
            self.restricoes_professores[professor].append([hora, dia])

    # Metodo que adiciona uma restricao a lista de restricoes das turmas
    def adicionar_restricoes_turmas(self, turma, hora, dia):
        # Se a turma ja tiver uma restricao na lista
        if turma in self.restricoes_turmas:
            self.restricoes_turmas.get(turma).append([hora, dia])
        # Se a turma nao tiver uma restricao na turma
        else:
            # Cria uma lista para guardar as restricoes
            self.restricoes_turmas[turma] = []
            # Adiciona a restricao a lista
            self.restricoes_turmas[turma].append([hora, dia])

    # Metodo que adiciona uma preferencia a lista de preferencias dos professores
    def adicionar_preferencias_professores(self, professor, hora, dia):
        # Se o professor ja tiver uma preferencia na lista
        if professor in self.preferencias_professores:
            self.preferencias_professores.get(professor).append([hora, dia])
        # Se o professor nao tiver uma preferencia na lista
        else:
            # Cria uma lista para guardar as preferencias
            self.preferencias_professores[professor] = []
            # Adiciona a preferencia a lista
            self.preferencias_professores[professor].append([hora, dia])

    # Metodo que incrementa as preferencias atendidas
    def incrementar_preferencias_atendidas(self, professor):
        if professor in self.preferenciais_atendidas:
            # Se o professor ja tem preferencias atendidas, incrementa o valor
            self.preferenciais_atendidas[professor] = self.preferenciais_atendidas.get(professor) + 1
        else:
            # Se essa eh a primeira preferencia atendida do professor, atribui
            # o valor 1
            self.preferenciais_atendidas[professor] = 1

    # Metodo que verifica as restricoes do enunciado
    # Restricao 1: Nao pode ter duas aulas com o mesmo professor no mesmo horario
    # Restricao 2: Nao pode ter duas aulas para uma mesma turma no mesmo horario
    def verificar_restricoes(self):
        for vertice1 in self.vertices:
            for vertice2 in self.vertices:
                if vertice1 != vertice2:
                    # Verifica se os vertices possuem um mesmo professor
                    # Seguindo o que o enunciado do trabalho fala: nao eh permitida
                    # a alocacao de duas aulas com o mesmo professor no mesmo horario
                    if vertice1.professor == vertice2.professor:
                        self.adicionar_aresta(vertice1, vertice2)
                    # Verifica se os vertices possuem uma mesma turma
                    # Seguindo o que o enunciado do trabalho fala: nao eh permitida
                    # a alocacao de duas aulas para a mesma turma no mesmo horario
                    if vertice1.turma == vertice2.turma:
                        self.adicionar_aresta(vertice1, vertice2)

    # Adiciona uma aresta nao-direcional ao vertice
    def adicionar_aresta(self, vertice1, vertice2):
        vertice1.adicionar_adjacente(vertice2)
        vertice2.adicionar_adjacente(vertice1)

    # Realiza a coloracao aplicando o Algoritmo Dsatur
    def dsatur(self):
        # Copia a lista de vertices para realizar a coloracao
        lista_para_colorir = self.vertices.copy()
        # Ordena em ordem decrescente a lista que sera usada na coloracao
        lista_para_colorir.sort(key=lambda vertice: vertice.get_grau(), reverse=True)
        # Atribui a cor 0 para o vertice de maior grau
        lista_para_colorir[0].cor = 0
        # Decrementa a variavel que armazena a quantidade de vertices nao coloridos
        self.quantidade_vertices_nao_coloridos -= 1
        # Remove o vertice colorido da lista
        lista_para_colorir.pop(0)
        # Executa o algoritmo enquanto a lista com os vertices para colorir nao
        # esteja vazia
        while lista_para_colorir:
            # Seleciona o proximo vertice para colorir
            proximo = self.proximo_vertice(lista_para_colorir)
            # Colore o vertice com a menor cor disponivel
            proximo.cor = proximo.menor_cor_disponivel(self.horarios, self.restricoes_professores)
            # Decrementa a variavel que armazena a quantidade de vertices nao coloridos
            self.quantidade_vertices_nao_coloridos -= 1
            # Remove o vertice colorido da lista
            lista_para_colorir.remove(proximo)

    # Metodo que retorna o proximo vertice a ser colorido
    def proximo_vertice(self, lista_vertices):
        # Dicionario para as saturacoes
        saturacoes = {}
        # Dicionario para os graus
        graus = {}
        # Loop que atribui as saturacoes e os graus aos dicionarios
        # Em ambos dicionarios, a chave eh o vertice e o valor eh a saturacao ou
        # o grau
        for vertice in lista_vertices:
            saturacoes[vertice] = vertice.get_saturacao()
            graus[vertice] = vertice.get_grau()
        if len(saturacoes):
            # Seleciona a maior (ou maiores) saturacao (ou saturacoes)
            # Se tiver mais de um vertice com a maior saturacao, o vertice com
            # maior grau eh selecionado
            maior_saturacao = max(saturacoes.values())
            maiores_saturacao = {v: saturacao for v, saturacao in graus.items() if saturacoes[v] == maior_saturacao}
            # Retorna o vertice com maior grau dos vertices com maiores saturacao
            return max(maiores_saturacao, key = maiores_saturacao.get)

    # Imprime os resultados do algoritmo como solicitado no enunciado do trabalho
    def imprimir_terminal(self):
        print("{}:".format(self.nome_escola))
        print("Quantidade de cores: {}".format(self.quantidade_cores))
        print("Preferências atendidas pelo total de preferências: {}%".format(self.porcentagem_preferenciais_atendidas()))

    # Retornar os dados que devem ser escritos no arquivo
    def retornar_dados_arquivo(self):
        return [self.nome_escola, self.quantidade_cores, self.tempo_iteracao, self.quantidade_vertices_nao_coloridos, self.preferenciais_atendidas]

    # Metodo que verifica se as cores (horarios) estao de acordo com as restricoes
    # dos professores
    def verificar_restricoes_professores(self):
        for vertice in self.vertices:
            # Verifica se o professor tem alguma restricao
            if vertice.professor in self.restricoes_professores:
                # Para cada restricao do professor, verifica se a restricao
                # entra em conflito com a cor do vertice
                for restricao in self.restricoes_professores.get(vertice.professor):
                    # Compara a restricao com o horario relativo a cor atual
                    if restricao[0] == self.horarios[vertice.cor][0] and restricao[1] == self.horarios[vertice.cor][1]:
                        vertice.melhor_cor_disponivel(self.horarios)

    # Metodo que verifica se existe tres ou mais aulas geminadas
    def verificar_geminadas(self):
        # Calcula a quantidade de aulas por dia
        aulas_por_dia = len(self.horarios) / 5
        # Ordena de forma crescente a lista de vertices por cor (horarios) para
        # melhorar a eficiencia da busca da cor
        self.vertices.sort(key=lambda vertice: vertice.cor)
        # Loop triplo que verifica se existe tres aulas com a mesma materia
        # seguidas
        for vertice1 in self.vertices:
            for vertice2 in self.vertices:
                for vertice3 in self.vertices:
                    if vertice1 != vertice2 and vertice2 != vertice3 and vertice1 != vertice3:
                        # Verifica se as aulas sao da mesma materia
                        if (vertice1.materia == vertice2.materia and vertice2.materia == vertice3.materia):
                            # Verifica se as aulas sao para a mesma turma
                            if (vertice1.turma == vertice2.turma and vertice2.turma == vertice3.turma):
                                # Verifica se as aulas sao seguidas
                                if ((vertice3.cor + 1) == vertice2.cor and (vertice2.cor + 1) == vertice1.cor):
                                    # Verifica se aulas estao no mesmo dia
                                    if (math.ceil(vertice1.cor / aulas_por_dia) == math.ceil(vertice2.cor / aulas_por_dia) and math.ceil(vertice2.cor / aulas_por_dia) == math.ceil(vertice3.cor / aulas_por_dia)):
                                        # Troca a aula para a melhor cor disponivel
                                        vertice3.melhor_cor_disponivel(self.horarios)

    # Metodo que verifica se existe grande janelas de horarios para uma turma
    def verificar_janelas(self):
        # Calcula a quantidade de aulas por dia
        aulas_por_dia = len(self.horarios) / 5
        # Ordena de forma crescente a lista de vertices por cor (horarios) para
        # melhorar a eficiencia da busca da cor
        self.vertices.sort(key=lambda vertice: vertice.cor)
        # Loop duplo que verifica se existe janelas entre duas aulas para mesma
        # materia
        for vertice1 in self.vertices:
            for vertice2 in self.vertices:
                if vertice1 != vertice2:
                    # Verifica se as aulas sao da mesma turma
                    if vertice1.turma == vertice2.turma:
                        # Verifica se aulas estao no mesmo dia
                        if math.ceil(vertice1.cor / aulas_por_dia) == math.ceil(vertice2.cor / aulas_por_dia):
                            # Verifica se tem uma janela de pelo menos dois horarios
                            if vertice1.cor + 1 <= vertice2.cor:
                                # Troca a aula para a melhor cor disponivel
                                vertice2.cor = vertice2.cor_disponivel_janela(vertice1, aulas_por_dia, self.horarios)

    # Metodo que verifica as preferencias dos professores
    def verificar_preferencias(self):
        # Loop para verifica todos os vertices e verificar se tem como atender a
        # preferencia do professor do vertice
        for vertice in self.vertices:
            # Verifica se o professor tem uma preferencia na lista de preferencia
            if vertice.professor in self.preferencias_professores:
                # Loop que percorre todas as preferecias do professor
                for preferencia in self.preferencias_professores.get(vertice.professor):
                    # Se o tem essa preferencia na lista de horarios
                    if preferencia in self.horarios:
                        # Verifica se eh possivel atender a preferencia do professor
                        # Se o for possivel, no proprio metodo de verificacao a
                        # a cor eh alterada
                        if vertice.verificar_preferencia(self.horarios.index(preferencia)):
                            self.incrementar_preferencias_atendidas(vertice.professor)

    # Metodo que calcula a porcentagem de preferencias atendidas
    def porcentagem_preferenciais_atendidas(self):
        total_preferencias = 0
        for professor in self.preferencias_professores.values():
            total_preferencias += len(professor)
        total_preferencias_atendidas = 0
        for atendida in self.preferenciais_atendidas.values():
            total_preferencias_atendidas += len(professor)
        valor = ((total_preferencias_atendidas / total_preferencias) * 100)
        # Retorna a porcentagem com duas casas decimais
        return ("%.2f" % valor)

# Metodo que escreve o resultado no arquivo
# O metodo usa uma lista (lista 1) com os dados
# Em cada posicao da lista dados tem um lista (lista 2) com os dados de uma escola
#   Na posicao 0 da lista 2, esta o nome da escola
#   Na posicao 1 da lista 2, esta a quantidade de horarios (ou cores) utilizada
#       na coloracao
#   Na posicao 2 da lista 2, esta o tempo (em segundos) do tempo que o algoritmo
#       levou para ser executado
#   Na posicao 3 da lista 2, esta a quantidade de vertices nao lidos
#   Na posicao 4 da lista 2, esta uma lista 3 com as preferencis atendidas para
#       para cada professor
#       Em cada posicao da lista 3, tem uma tupla com o identificador do
#           # professor e a quantidade de preferencias atendidas
def escrever_arquivo(dados, nome_arquivo):
    # Abre o arquivo para escrita
    # Se o arquivo existe, ele apaga os dados e escreve por cima
    # Se o arquivo nao existe, um arquivo vazio eh criado
    arquivo = open(nome_arquivo, 'w')
    arquivo.write("Resultados:\n")
    arquivo.write("Quantidade de horarios utilizadas (cores):\n")
    # Salva no arquivo a quantidade de horario utilizada por cada escola
    for dado in dados:
        arquivo.write("{}: {}\n".format(dado[0], dado[1]))
    arquivo.write("Tempo para iteracao do algoritmo (em segundos):\n")
    # Salva no arquivo o tempo gasto por cada algoritmo
    for dado in dados:
        arquivo.write("{}: {}\n".format(dado[0], round(dado[2], 2)))
    arquivo.write("Quantidade de vertices nao coloridos:\n")
    # Salva no arquivo a quantidade de vertices noa coloridos
    for dado in dados:
        arquivo.write("{}: {}\n".format(dado[0], dado[3]))
    arquivo.write("Quantidade de preferencias nao atendidas para cada professor (somente dos professores que possuem preferencias):\n")
    # Salva no arquivo a quantidade de preferencias atendidas por cada professor
    # (somente se o professor tiver preferencias) em cada escola
    for dado in dados:
        # Salva o nome da escola
        arquivo.write("{}:\n".format(dado[0]))
        if dado[4]:
            for professor, quantidade in dado[4].items():
                # Salva o nome do professor e a quantidade de preferenciais atendidas
                arquivo.write("{}: {}\n".format(professor, quantidade))
    # Fecha o arquivo
    arquivo.close()

def main():
    # Lista para armazena os dados de cada grafo
    dados = []
    # Grafo 1
    grafo1 = Grafo("../data/Escola_A.xlsx", "Escola A")
    # Imprime os resultados no terminal
    grafo1.imprimir_terminal()
    # Adiciona os resultados desse grafo a lista de resultados
    dados.append(grafo1.retornar_dados_arquivo())
    # Grafo 2
    grafo2 = Grafo("../data/Escola_B.xlsx", "Escola B")
    # Imprime os resultados no terminal
    grafo2.imprimir_terminal()
    # Adiciona os resultados desse grafo a lista de resultados
    dados.append(grafo2.retornar_dados_arquivo())
    # Grafo 3
    grafo3 = Grafo("../data/Escola_C.xlsx", "Escola C")
    # Imprime os resultados no terminal
    grafo3.imprimir_terminal()
    # Adiciona os resultados desse grafo a lista de resultados
    dados.append(grafo3.retornar_dados_arquivo())
    # Grafo 4
    grafo4 = Grafo("../data/Escola_D.xlsx", "Escola D")
    # Imprime os resultados no terminal
    grafo4.imprimir_terminal()
    # Adiciona os resultados desse grafo a lista de resultados
    dados.append(grafo4.retornar_dados_arquivo())
    # Escreve no arquivo texto os resultados
    escrever_arquivo(dados, "../data/Resultados.txt")

if __name__ == "__main__":
    main()
