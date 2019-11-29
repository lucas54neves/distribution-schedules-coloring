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
# from tabulate import tabulate
import time

class Horario:
    def __init__(self, hora, dia):
        self.hora = hora
        self.dia = dia

    def __str__(self):
        return "Hora: " + str(self.hora) + " - Dia: " + str(self.dia)

# A classe Escolha representa a preferencia de horario ou a restricao de horario
class Escolha:
    def __init__(self, identificador, horario):
        self.identificador = identificador
        self.horario = horario

    def __str__(self):
        return "Identificador: " + str(self.identificador) + " " + str(self.horario)

class Vertice:
    def __init__(self, indice, materia, professor, turma):
        self.indice = indice
        self.materia = materia
        self.professor = professor
        self.turma = turma
        self.adjacentes = []
        self.cor = None

    def adicionar_adjacente(self, adjacente):
        self.adjacentes.append(adjacente)

    def eh_adjacente(self, possivel_adjacente):
        for adjacente in self.adjacentes:
            if adjacente == possivel_adjacente:
                return True
        return False

    # Retorna o grau do vertice
    def get_grau(self):
        return len(self.adjacentes)

    # Retorna o grau de saturacao do vertice
    # A saturacao eh o numero de diferentes cores para qual o vertice eh adjacente
    def get_saturacao(self):
        saturacao = 0
        for adjacente in self.adjacentes:
            if adjacente.cor is not None:
                saturacao += 1
        return saturacao

    def menor_cor_disponivel(self):
        menor = 0

        for vertice in self.adjacentes:
            if vertice.cor == menor:
                menor += 1

        return menor

    def __str__(self):
        return "Vertice " + str(self.indice) + " =>" + " Materia: " + str(self.materia) + " Professor: " + str(self.professor) + " Turma: " + str(self.turma)

class Grafo:
    def __init__(self, nome_arquivo, nome_escola, algoritmo_selecionado):
        # Lista que armazena os vertices do grafo
        self.vertices = []
        # Lista que armazena as horas disponiveis para aula por dia
        self.horas = []
        # Lista que armazena os horarios disponiveis para aula por semana
        self.horarios = []
        # Lista que armazena as restricoes de horarios dos professores
        self.restricoes_professores = []
        # Lista que armazena as restricoes de horarios das turmas
        self.restricoes_turmas = []
        # Lista que armazena as preferencias de horarios dos professores
        self.preferencias_professores = []
        # Variavel para guardar a quantidade de vertices coloridos
        self.vertices_coloridos = 0
        # Nome da escola para imprimir no resultado
        self.nome_escola = nome_escola
        # Metodo que realiza a leitura do arquivo
        self.ler_arquivo(nome_arquivo)
        # Metodo que verifica todas as restricoes
        self.verificar_restricoes()
        # Metodo que colere o grafo
        inicio = time.time()
        self.colorir(algoritmo_selecionado)
        fim = time.time()
        self.tempo_iteracao = fim - inicio

        # Metodo que imprime o relatorio no terminal
        self.imprimir_terminal()

    def quantidade_vertices(self):
        return len(self.vertices)

    def ler_arquivo(self, nome_arquivo):
        planilha = xlrd.open_workbook(nome_arquivo)
        self.ler_dados(planilha)
        self.ler_configuracoes(planilha)
        self.ler_restricoes_professores(planilha)
        self.ler_restricoes_turma(planilha)
        self.ler_preferencias(planilha)

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
                    self.adicionar_vertice(materia, professor, turma)


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

    def ler_restricoes_professores(self, planilha):
        # Pega a terceira aba da planilha
        # Essa aba estao as restricoes de horarios de cada professor
        aba = planilha.sheet_by_index(2)

        # Loop para leitura das linhas
        for i in range(aba.nrows):
            if i != 0:
                valores = aba.row_values(i)

                # Pega o numero relativo ao professor
                auxiliar = valores[0].split()
                professor = int(auxiliar[1])

                # Pega a hora da preferencia de horario
                hora = float(valores[1])

                # Pega o dia da preferencia de horario
                dia = valores[2].encode('utf-8')

                self.adicionar_restricoes_professores(professor, hora, dia)

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
                dia = valores[2].encode('utf-8')

                self.adicionar_restricoes_turmas(turma, hora, dia)

    def ler_preferencias(self, planilha):
        # Pega a quinta aba da planilha
        # Essa aba estao as preferencias de horarios de cada professor
        aba = planilha.sheet_by_index(4)

        # Loop para leitura das linhas
        for i in range(aba.nrows):
            if i != 0:
                valores = aba.row_values(i)

                # Pega o numero relativo ao professor
                auxiliar = valores[0].split()
                professor = int(auxiliar[1])

                # Pega a hora da preferencia de horario
                hora = float(valores[1])

                # Pega o dia da preferencia de horario
                dia = valores[2].encode('utf-8')

                self.adicionar_preferencias_professores(professor, hora, dia)

    def adicionar_vertice(self, materia, professor, turma):
        self.vertices.append(Vertice(len(self.vertices), materia, professor, turma))

    def adicionar_hora(self, hora):
        self.horas.append(hora)

    def criacao_cores(self):
        dias = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]

        for dia in dias:
            for hora in self.horas:
                self.adicionar_horario(hora, dia)

    def adicionar_horario(self, hora, dia):
        self.horarios.append(Horario(hora, dia))

    def adicionar_restricoes_professores(self, professor, hora, dia):
        self.restricoes_professores.append(Escolha(professor, Horario(hora, dia)))

    def adicionar_restricoes_turmas(self, turma, hora, dia):
        self.restricoes_turmas.append(Escolha(turma, Horario(hora, dia)))

    def adicionar_preferencias_professores(self, professor, hora, dia):
        self.preferencias_professores.append(Escolha(professor, Horario(hora, dia)))

    def verificar_restricoes(self):
        for vertice1 in self.vertices:
            for vertice2 in self. vertices:
                # A verificacao so ira ocorrer se os dois vertices forem diferentes
                # e se os vertices nao forem adjacentes. Se os vertices ja forem
                # adjacentes, isso significa que ja existe uma restricao entre os dois vertices
                if vertice1 != vertice2:
                    # Verifica se os vertices possuem uma mesma materia
                    # Seguindo o que o enunciado do trabalho fala: nao eh permitida
                    # a alocacao de duas aulas com a mesma materia no mesmo horario
                    if vertice1.materia == vertice2.materia and not vertice1.eh_adjacente(vertice2):
                        self.adicionar_aresta(vertice1, vertice2)

                    # Verifica se os vertices possuem um mesmo professor
                    # Seguindo o que o enunciado do trabalho fala: nao eh permitida
                    # a alocacao de duas aulas com o mesmo professor no mesmo horario
                    if vertice1.professor == vertice2.professor and not vertice1.eh_adjacente(vertice2):
                        self.adicionar_aresta(vertice1, vertice2)

                    # Verifica se os vertices possuem uma mesma turma
                    # Seguindo o que o enunciado do trabalho fala: nao eh permitida
                    # a alocacao de duas aulas para a mesma turma no mesmo horario
                    if vertice1.turma == vertice2.turma and not vertice1.eh_adjacente(vertice2):
                        self.adicionar_aresta(vertice1, vertice2)

    def adicionar_aresta(self, vertice1, vertice2):
        vertice1.adicionar_adjacente(vertice2)
        vertice2.adicionar_adjacente(vertice1)

    # Realiza a coloracao de acordo com o algoritmo selecionado
    # [1] Heristica Gulosa
    # [2] Algoritmo Dsatur
    def colorir(self, algoritmo_selecionado):
        if algoritmo_selecionado == 1:
            self.heuristica_gulosa()
        elif algoritmo_selecionado == 2:
            self.dsatur()
        else:
            print("Nenhum algoritmo selecionado")

    def heuristica_gulosa(self):
        self.vertices[0].cor = 0
        for vertice in self.vertices:
            if vertice.cor == None:
                vertice.cor = vertice.menor_cor_disponivel()

    def dsatur(self):
        # Copia a lista de vertices para realizar a coloracao
        lista_para_colorir = self.vertices.copy()

        # Ordena em ordem decrescente a lista que sera usada na coloracao
        lista_para_colorir.sort(key=lambda vertice: vertice.get_grau(), reverse=True)

        # Atribui a cor 0 para o vertice de maior grau
        lista_para_colorir[0].cor = 0

        # Remove o vertice colorido da lista
        lista_para_colorir.pop(0)

        # Executa o algoritmo enquanto a lista com os vertices para colorir nao
        # esteja vazia
        while lista_para_colorir:
            # Seleciona o proximo vertice para colorir
            proximo = self.proximo_vertice(lista_para_colorir)

            # Colore o vertice com a menor cor disponivel
            proximo.cor = proximo.menor_cor_disponivel()

            # Remove o vertice colorido da lista
            lista_para_colorir.remove(proximo)

    def proximo_vertice(self, lista_vertices):
        saturacoes = {}
        graus = {}

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
        print("Quantidade de cores: {}".format(max(self.vertices, key =  lambda vertice: vertice.cor).cor))
        print("Preferências atendidas pelo total de preferências: {}".format(0))

    # Retornar os dados que devem ser escritos no arquivo
    def retornar_dados_arquivo(self):
        return [self.nome_escola, self.quantidade_cores, self.tempo_iteracao, self.quantidade_vertices_nao_coloridos, self.get_preferenciais_atendidas()]

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
    arquivo.write("Resultados:")
    arquivo.write("Quantidade de horarios utilizadas (cores):")
    # Salva no arquivo a quantidade de horario utilizada por cada escola
    for dado in dados:
        arquivo.write("{}: {}".format(dado[0], dado[1]))
    arquivo.write("Tempo para iteracao do algoritmo (em segundos):")
    # Salva no arquivo o tempo gasto por cada algoritmo
    for dado in dados:
        arquivo.write("{}: {}".format(dado[0], dado[2]))
    arquivo.write("Quantidade de vertices nao coloridos:")
    # Salva no arquivo a quantidade de vertices noa coloridos
    for dado in dados:
        arquivo.write("{}: {}".format(dado[0], dado[3]))
    arquivo.write("Quantidade de preferencias nao atendidas para cada professor (somente dos professores que possuem preferencias):")
    # Salva no arquivo a quantidade de preferencias atendidas por cada professor
    # (somente se o professor tiver preferencias) em cada escola
    for dado in dados:
        # Salva o nome da escola
        arquivo.write("{}:".format(dado[0]))
        for professor in dado[4]:
            # Salva o nome do professor e a quantidade de preferenciais atendidas
            arquivo.write("{}: {}".format(professor[0], professor[1]))
    # Fecha o arquivo
    arquivo.close()

def main():
    print("Opcoes de algoritmos")
    print("[1] Heuristica Gulosa")
    print("[2] Algoritmo Dsatur")
    algoritmo = int(input("Entre com o algoritmo desejado: "))
    # dados = []
    grafo1 = Grafo("../dados/Escola_A.xlsx", "Escola A", algoritmo)
    # dados.append(grafo1.retornar_dados_arquivo())
    grafo2 = Grafo("../dados/Escola_B.xlsx", "Escola B", algoritmo)
    # dados.append(grafo2.retornar_dados_arquivo())
    grafo3 = Grafo("../dados/Escola_C.xlsx", "Escola C", algoritmo)
    # dados.append(grafo3.retornar_dados_arquivo())
    grafo4 = Grafo("../dados/Escola_D.xlsx", "Escola D", algoritmo)
    # dados.append(grafo4.retornar_dados_arquivo())
    # escrever_arquivo(dados, "Resultados.txt")

if __name__ == "__main__":
    main()
