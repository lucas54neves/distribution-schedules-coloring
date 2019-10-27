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

    def imprimir(self):
        print(self.indice, self.horario.get_hora(), self.horario.get_dia())

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
        print(self.indice, self.horario.get_hora(), self.horario.get_dia())

# Classe que representa os vertices
class Vertice:
    def __init__(self, indice, disciplina):
        self.indice = indice
        self.disciplina = disciplina
        self.cor = None
        self.grau = 0
        self.saturacao = 0

    def get_indice(self):
        return self.indice

    def get_disciplina(self):
        return self.disciplina

    def get_cor(self):
        return self.cor

    def get_grau(self):
        return self.grau

    def get_saturacao(self):
        return self.saturacao

    def set_grau(self, novo_grau):
        self.grau = novo_grau

    def set_cor(self, nova_cor):
        self.cor = nova_cor

    def aumentar_saturacao(self):
        self.saturacao += 1

    def imprimir(self):
        print(self.indice, self.grau)

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
        self.lista_horas = []
        # Lista que guarda as restricoes de horarios dos professores
        self.lista_restricoes_professores = []
        # Lista que guarda as cores relativas aos horarios
        self.lista_cores = []
        # Lista que guarda as restricoes dos horarios das turmas
        self.lista_restricoes_turmas = []
        # Lista que guarda as preferencias de cada professor
        self.lista_preferencias_professores = []

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

                self.adicionar_vertice(i - 1, Disciplina(indice, materia, turma, professor_indice, quantidade_aulas))

        # Apenas depois da leitura de todas disciplinas (vertices) eh possivel
        # Criar a lista de adjacencia porque precisa da quantidade de vertices
        self.construir_lista_adjacencia()

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

    def adicionar_vertice(self, indice, disciplina):
        self.lista_vertices.append(Vertice(indice, disciplina))

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
                    # nao eh permitida a alocacao de duas aulas para um
                    # mesmo professor no mesmo horario
                    if vertice1.get_disciplina().get_professor() == vertice2.get_disciplina().get_professor():
                        self.criar_aresta(vertice1.get_indice(), vertice2.get_indice())
                    # nao pode haver duas aulas para uma mesma turma no
                    # mesmo horario
                    if vertice1.get_disciplina().get_turma() == vertice2.get_disciplina().get_turma():
                        self.criar_aresta(vertice1.get_indice(), vertice2.get_indice())

    def adicionar_cores(self):
        dias = ("Segunda", "Terça", "Quarta", "Quinta", "Sexta")

        # indice para as cores
        i = 0
        for dia in dias:
            for hora in self.lista_horas:
                self.lista_cores.append(Cor(i, Horario(hora, dia)))
                i += 1

    def aumentar_saturacao(self, vertice):
        for adjacente in self.lista_adjacencia[vertice]:
            self.lista_vertices[adjacente].aumentar_saturacao()

    def menor_cor_disponivel(self, vertice):
        cores_disponiveis = [cor for cor self.lista_cores]
        for adjacente in self.lista_adjacencia[vertice]:
            if self.lista_vertices[adjacente].get_cor != None:
                cores_disponiveis.remove(self.lista_vertices[adjacente].get_cor)
        cores_disponiveis.sort(key=lambda cor: cor.get_indice)
        return cores_disponiveis[0]

    # Metodo que colore os vertices
    def colore(self):
        # Calcular os graus
        for vertice in self.lista_vertices:
            vertice.set_grau(len(self.lista_adjacencia[vertice.get_indice()]))

        # Ordena os vertices em ordem decrescente de grau
        self.lista_vertices.sort(key=lambda vertice: vertice.get_grau(), reverse=True)

        self.lista_vertices[0].set_cor(self.lista_cores[0])
        self.aumentar_saturacao(self.lista_vertices[0].get_indice())

        coloridos = 1
        # Enquanto ainda existir um vertice descolorido
        while coloridos <= len(self.lista_vertices):
            # Ordena os vertices em ordem decrescente de grau de saturacao
            self.lista_vertices.sort(key=lambda vertice: vertice.get_saturacao(), reverse=True)

            self.lista_vertices[0].set_cor()

        for vertice in self.lista_vertices:
            if vertice.get_cor() == None:
                cor = None
            else:
                cor = vertice.get_cor().get_indice()
            print(vertice.get_indice(), cor, vertice.get_grau())

grafo = Grafo()
grafo.leitura("dados/Escola_A.xlsx")
grafo.verificar_restricoes()
# grafo.imprimir_lista_adjacendia()
grafo.colore()