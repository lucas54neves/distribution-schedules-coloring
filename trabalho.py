#!/usr/bin/python
# -*- coding: latin-1 -*-

import xlrd
import datetime
import math
import time

# Classe que representa as restricoes de horarios do professores
class Restricao:
    def __init__(self, indice_professor, horario, dia):
        self.indice_professor = indice_professor
        self.horario = horario
        self.dia = dia

    def get_indice_professor(self):
        return self.indice_professor

    def get_horario(self):
        return self.horario

    def get_dia(self):
        return self.dia

    def imprimir(self):
        print(self.indice_professor, self.horario, self.dia)

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

    def imprimir(self):
        print(self.indice, self.materia, self.turma, self.professor, self.quantidade_aulas)

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
        print(self.indice, self.horario)

# Classe que representa os vertices
class Vertice:
    def __init__(self, indice, disciplina):
        self.indice = indice
        self.disciplina = disciplina
        self.cor = None

    def get_indice(self):
        return self.indice

    def get_disciplina(self):
        return self.disciplina

    def get_cor(self):
        return self.cor

    def imprimir(self):
        print("Vertice {} {}".format(self.indice, self.cor))
        self.disciplina.imprimir()

# Classe que representa o grafo
class Grafo:
    def __init__(self):
        # Quantidade de disciplinas
        self.quantidade_vertices = 0
        # Lista que guarda as disciplinas
        self.lista_vertices = []
        # Lista de adjacencia entre os vertices
        self.lista_adjacencia = []
        # Lista que guarda os horarios
        self.lista_horarios = []
        # Lista que guarda as restricoes de horarios dos professores
        self.lista_restricoes_professores = []
        # Lista que guarda as cores relativas aos horarios
        self.lista_cores = []

    def leitura(self, nome_arquivo):
        # Abre o arquivo
        planilha = xlrd.open_workbook(nome_arquivo)

        # Realiza a leitura da aba Dados
        self.leitura_dados(planilha)

        # Realiza a leitura da aba Configuracoes
        self.leitura_configuracoes(planilha)

        # Realiza a leitura da aba Restricoes
        self.leitura_restricoes(planilha)

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

                self.adicionar_vertice(i - 1, Disciplina(indice, materia, turma, professor_indice, quantidade_aulas))

        # Apenas depois da leitura de todas disciplinas (vertices) eh possivel
        # Criar a lista de adjacencia porque precisa da quantidade de vertices
        self.construir_lista_adjacencia()

        # for vertice in self.lista_vertices:
        #     vertice.imprimir()

    def leitura_configuracoes(self, arquivo):
        # Pega a segunda aba da planilha, a aba Configuracoes
        aba = arquivo.sheet_by_index(1)

        # Loop para leitura dos dados
        for i in xrange(aba.nrows):
            if i != 0:
                valores = aba.row_values(i)
                horario = float(valores[0])
                # x = float(valores[0]) * 24 * 3600
                #self.adicionar_horario(datetime.time(int(x/3600), int((x%3600)/60), int(x%60)))
                # self.adicionar_horario(time.strftime('%H:%M:%S',x))
                #time.strftime('%H:%M:%S', time.gmtime(12345))
                self.adicionar_horario(horario)

        self.adicionar_cores()

        # Teste de leitura
        # print("Configuracoes")
        # for i in self.lista_horarios:
        #     print(i)

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

                # Pega o horario
                horario = valores[1]

                # Pega o dia da semana
                dia = valores[2].encode('utf-8')

                self.adicionar_restricao(indice_professor, horario, dia)

        # for i in self.lista_restricoes_professores:
        #     i.imprimir()

    def adicionar_vertice(self, indice, disciplina):
        self.lista_vertices.append(Vertice(indice, disciplina))

    def adicionar_horario(self, horario):
        self.lista_horarios.append(horario)

    def adicionar_restricao(self, indice_professor, horario, dia):
        self.lista_restricoes_professores.append(Restricao(indice_professor, horario, dia))

    def construir_lista_adjacencia(self):
        self.quantidade_vertices = len(self.lista_vertices)
        for i in range(self.quantidade_vertices):
            self.lista_adjacencia.append([])

    def criar_aresta(self, u, v):
        self.lista_adjacencia[u].append(v)

    def imprimir(self):
        for vertice in self.lista_vertices:
            vertice.imprimir()

    def imprimir_lista_adjacendia(self):
        for i in range(self.quantidade_vertices):
            print(i, self.lista_adjacencia[i])

    def verificar_restricoes(self):
        for vertice1 in self.lista_vertices:
            for vertice2 in self.lista_vertices:
                if vertice1 != vertice2:
                    if vertice1.get_disciplina().get_professor() == vertice2.get_disciplina().get_professor():
                        self.criar_aresta(vertice1.get_indice(), vertice2.get_indice())
                    if vertice1.get_disciplina().get_turma() == vertice2.get_disciplina().get_turma():
                        self.criar_aresta(vertice1.get_indice(), vertice2.get_indice())

    def adicionar_cores(self):
        dias = ("Segunda", "Terça", "Quarta", "Quinta", "Sexta")

        i = 0
        for dia in dias:
            for horario in self.lista_horarios:
                self.lista_cores.append(Cor(i, (horario, dia)))
                i += 1

        for cor in self.lista_cores:
            cor.imprimir()

grafo = Grafo()
grafo.leitura("dados/Escola_A.xlsx")
grafo.verificar_restricoes()
# grafo.imprimir_lista_adjacendia()
