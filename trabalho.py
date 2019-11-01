#!/usr/bin/python
# -*- coding: utf-8 -*-

import xlrd
import datetime
import math
import time

# Classe que representa o horario
class Horario:
    def __init__(self, hora, dia):
        self.hora = hora
        self.dia = dia

    def get_hora(self):
        return self.hora

    def get_dia(self):
        return self.dia

    def __str__(self):
        return "Horario: " + str(self.hora) + " - Dia:" + str(self.dia)

# Classe que representa as restricoes de horarios dos professores ou das turma
class Restricao:
    def __init__(self, indice, horario):
        # Indice do professor ou da turma
        self.indice = indice
        # Horario de restricao
        self.horario = horario

    def get_indice(self):
        return self.indice

    def get_horario(self):
        return self.horario

    def __str__(self):
        return "Restricao/Preferencia: " + str(self.indice) + str(self.horario)


# Classe que representa as disciplinas
class Disciplina:
    def __init__(self, indice, materia, turma, professor, quantidade_aulas):
        # Indice da disciplina
        self.indice = indice
        # Letra relativa a materia
        self.materia = materia
        # Numero relativo a tuma
        self.turma = turma
        # Indice do professor
        self.professor = professor
        # Quantidade de aulas da disciplina
        self.quantidade_aulas = quantidade_aulas

    def get_indice(self):
        return self.indice

    def get_materia(self):
        return self.materia

    def get_turma(self):
        return self.turma

    def get_professor(self):
        return self.professor

    def get_quantidade_aulas(self):
        return self.quantidade_aulas

    def __str__(self):
        return "Discuplina: " + str(self.indice) + " - Materia: " + str(self.materia) + " - Turma: " + str(self.turma) + " - Professor: " + str(self.professor) + " - Quantidade de aulas: " + str(self.quantidade_aulas)

# Classe que representa as cores
class Cor:
    def __init__(self, indice, horario):
        self.indice = indice
        self.horario = horario

    def get_indice(self):
        return self.indice

    def get_horario(self):
        return self.horario

    def imprimir(self):
        print(self.indice, self.horario.get_hora(), self.horario.get_dia())

    def __str__(self):
        return "Cor: " + str(self.indice) + " - Hora :" + str(self.horario.get_hora()) + " - Dia: " + str(self.horario.get_dia())

# Classe que representa os vertices
class Vertice:
    def __init__(self, indice, disciplina):
        self.indice = indice
        self.adjacentes = []
        self.disciplina = disciplina
        self.cor = None

    def get_indice(self):
        return self.indice

    def get_adjacentes(self):
        return self.adjacentes

    def get_disciplina(self):
        return self.disciplina

    def get_cor(self):
        return self.cor

    def get_grau(self):
        return len(self.adjacentes)

    def get_saturacao(self):
        return sum(vertice.get_cor() is not None for vertice in self.adjacentes)

    def set_grau(self, novo_grau):
        self.grau = novo_grau

    def set_cor(self, nova_cor):
        self.cor = nova_cor

    def set_saturacao(self, nova_saturacao):
        self.saturacao = nova_saturacao

    def adicionar_aresta(self, adjacente):
        self.adjacentes.append(adjacente)

    # Imprime o vertice
    def __str__(self):
        return "Vertice: " + str(self.indice) + " " + str(self.cor)

# Classe que representa o grafo
class Grafo:
    def __init__(self):
        # Lista que guarda as disciplinas
        self.vertices = []
        # Lista que guarda os horarios
        self.lista_horas = []
        # Lista que guarda as restricoes de horarios dos professores
        self.lista_restricoes_professores = []
        # Lista que guarda as cores relativas aos horarios
        self.cores = []
        # Lista que guarda as restricoes dos horarios das turmas
        self.lista_restricoes_turmas = []
        # Lista que guarda as preferencias de cada professor
        self.lista_preferencias_professores = []

    # Retorna a quantidade de vertices
    def quantidade_vertices(self):
        return len(self.vertices)

    # Adicionar um vertice ao grafo
    # O parametro eh a disciplina e o indice eh calculado durante a insercao
    def adicionar_vertice(self, disciplina):
        self.vertices.append(Vertice(len(self.vertices), disciplina))

    # Adiciona uma aresta ao grafo
    # Os parametros sao o indice do vertice (de origem da aresta) e o indice do
    # adjacente (ou seja, vertice de destino da aresta)
    def adicionar_aresta(self, vertice, adjacente):
        self.vertices[vertice].get_adjacentes().append(self.vertices[adjacente])

    def leitura(self, nome_arquivo):
        # Abre o arquivo
        planilha = xlrd.open_workbook(nome_arquivo)

        # Realiza a leitura da aba Dados
        self.leitura_dados(planilha)

        # Realiza a leitura da aba Configuracoes
        self.leitura_configuracoes(planilha)

        # Realiza a leitura da aba Restricoes
        self.leitura_restricoes(planilha)

        # Realiza a leitura da aba Restricoes Turma
        self.leitura_restricoes_turma(planilha)

        # Realiza a leitura da aba Preferencias
        self.leitura_preferencias(planilha)

    def leitura_dados(self, arquivo):
        # Pega a primeira aba da planilha, a aba Dados
        aba = arquivo.sheet_by_index(0)

        # Loop para leitura dos dados
        for i in xrange(aba.nrows):
            if i != 0:
                valores = aba.row_values(i)

                # Pega o indice da disciplina
                indice = i

                # Pega a letra correspondente a materia
                materia = str(valores[0])

                # Pega o numero da turma
                turma = int(valores[1])

                # Pega o indice do professor
                professor = valores[2].split()
                professor_indice = int(professor[1])

                # Pega a quantidade de aulas
                quantidade_aulas = int(valores[3])

                self.adicionar_vertice(Disciplina(indice, materia, turma, professor_indice, quantidade_aulas))

    def leitura_configuracoes(self, arquivo):
        # Pega a segunda aba da planilha, a aba Configuracoes
        aba = arquivo.sheet_by_index(1)

        # Loop para leitura dos dados
        for i in xrange(aba.nrows):
            if i != 0:
                valores = aba.row_values(i)
                hora = float(valores[0])
                self.adicionar_hora(hora)

        self.adicionar_cores()

    def leitura_restricoes(self, arquivo):
        # Pega a terceira aba da planilha, a aba Restricoes
        # Nessa aba esta os horarios indisponiveis para cada professor
        aba = arquivo.sheet_by_index(2)

        # Loop para leitura dos dados
        for i in xrange(aba.nrows):
            if i != 0:
                valores = aba.row_values(i)

                # Pega o indice do professor
                professor = valores[0].split()
                indice_professor = int(professor[1])

                # Pega a hora
                hora = valores[1]

                # Pega o dia da semana
                dia = valores[2].encode('utf-8')

                self.adicionar_restricao_professores(indice_professor, Horario(hora, dia))

    def leitura_restricoes_turma(self, arquivo):
        # Pega a quarta aba da planilha, a aba Restricoes Turma
        # Nessa aba esta os horarios de restricao para cada turma
        aba = arquivo.sheet_by_index(3)

        # Loop para leitura dos dados
        for i in xrange(aba.nrows):
            if i != 0:
                valores = aba.row_values(i)

                # Pega o numero da turma
                turma = int(valores[0])

                # Pega a hora
                hora = float(valores[1])

                # Pega o dia
                dia = valores[2].encode('utf-8')

                self.adicionar_restricao_turmas(turma, Horario(hora, dia))

    def leitura_preferencias(self, arquivo):
        # Pega a quinta aba da planilha, a aba Preferencias
        # Nessa aba esta os horarios de preferencias de cada professor
        aba = arquivo.sheet_by_index(4)

        # Loop para leitura dos dados
        for i in xrange(aba.nrows):
            if i != 0:
                valores = aba.row_values(i)

                # Pega o indice do professor
                professor = valores[0].split()
                indice_professor = int(professor[1])

                # Pega a hora
                hora = float(valores[1])

                # Pega o dia
                dia = valores[2].encode('utf-8')

                self.adicionar_preferencias_professores(indice_professor, Horario(hora, dia))

    def adicionar_hora(self, hora):
        self.lista_horas.append(hora)

    def adicionar_restricao_professores(self, indice_professor, horario):
        self.lista_restricoes_professores.append(Restricao(indice_professor, horario))

    def adicionar_restricao_turmas(self, turma, horario):
        self.lista_restricoes_turmas.append(Restricao(turma, horario))

    # Para adicionar as preferencias dos professores esta sendo aproveitada a
    # classe Restricao
    def adicionar_preferencias_professores(self, professor, horario):
        self.lista_preferencias_professores.append(Restricao(professor, horario))

    def verificar_restricoes(self):
        for vertice1 in self.vertices:
            for vertice2 in self.vertices:
                if vertice1 != vertice2:
                    if vertice1.get_disciplina().get_materia() == vertice2.get_disciplina().get_materia():
                        self.adicionar_aresta(vertice1.get_indice(), vertice2.get_indice())

                    # nao eh permitida a alocacao de duas aulas para um
                    # mesmo professor no mesmo horario
                    if vertice1.get_disciplina().get_professor() == vertice2.get_disciplina().get_professor():
                        self.adicionar_aresta(vertice1.get_indice(), vertice2.get_indice())
                    # nao pode haver duas aulas para uma mesma turma no
                    # mesmo horario
                    if vertice1.get_disciplina().get_turma() == vertice2.get_disciplina().get_turma():
                        self.adicionar_aresta(vertice1.get_indice(), vertice2.get_indice())

    def adicionar_cores(self):
        dias = ("Segunda", "Terça", "Quarta", "Quinta", "Sexta")

        # indice para as cores
        i = 0
        for dia in dias:
            for hora in self.lista_horas:
                self.cores.append(Cor(i, Horario(hora, dia)))
                i += 1

        for cor in self.cores:
            print(cor)

    # Metodo que colore os vertices
    def colorir(self):
        maior_grau = max(self.vertices, key = lambda vertice: vertice.get_grau())
        maior_grau.set_cor(self.menor_cor(maior_grau))

        proximo = self.proximo_colore(maior_grau)

        while proximo != None:
            proximo.set_cor(self.menor_cor(proximo))
            proximo = self.proximo_colore(maior_grau)


    # Retorna o proximo vertice a colorir
    def proximo_colore(self, vertice):
        saturacoes = {}
        graus = {}

        for adjacente in vertice.get_adjacentes():
            if adjacente.get_cor() == None:
                saturacoes[adjacente] = adjacente.get_saturacao()
                graus[adjacente] = adjacente.get_grau()

        if len(saturacoes):
            # Pega a maior (ou maiores) saturacao (ou saturacoes)
            # Se tiver mais de um vertice com a maior saturacao, o vertice com
            # maior grau eh retornado no final desse if
            maior_saturacao = max(saturacoes.values())
            maiores_saturacao = {v: saturacao for v, saturacao in graus.items() if saturacoes[v] == maior_saturacao}

            # Retorna o vertice com maior grau dos vertices com maiores saturacao
            return max(maiores_saturacao, key = maiores_saturacao.get)

    # Retorna a menor cor
    def menor_cor(self, vertice):
        menor = 0

        for adjacente in vertice.get_adjacentes():
            if adjacente.get_cor() == self.cores[menor]:
                menor += 1

        return self.cores[menor]

    def imprimir_vertices(self):
        for vertice in self.vertices:
            print(vertice)

grafo = Grafo()
grafo.leitura("dados/Escola_A.xlsx")
grafo.verificar_restricoes()
grafo.colorir()
grafo.imprimir_vertices()
