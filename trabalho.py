#!/usr/bin/python
# -*- coding: utf-8 -*-

import xlrd

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
    def __init__(self, indice, materia, professor, turma, quantidade_aulas):
        self.indice = indice
        self.materia = materia
        self.professor = professor
        self.turma = turma
        self.quantidade_aulas = quantidade_aulas
        self.adjacentes = []

    def adicionar_adjacente(self, adjacente):
        self.adjacentes.append(adjacente)

    def eh_adjacente(self, possivel_adjacente):
        for adjacente in self.adjacentes:
            if adjacente == possivel_adjacente:
                return True
        return False

    def __str__(self):
        return "Vertice " + str(self.indice) + " =>" + " Materia: " + str(self.materia) + " Professor: " + str(self.professor) + " Turma: " + str(self.turma) + " Aulas: " + str(self.quantidade_aulas)

class Grafo:
    def __init__(self, nome_arquivo):
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
        self.ler_arquivo(nome_arquivo)
        self.verificar_restricoes()
        #self.algoritmo_coloracao()
        self.imprimir_relatorio()

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

                # Adicionar o vertice com as informacoes coletas nessa linha da aba
                self.adicionar_vertice(materia, turma, professor, quantidade_aulas)

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

    def adicionar_vertice(self, materia, turma, professor, quantidade_aulas):
        self.vertices.append(Vertice(len(self.vertices), materia, turma, professor, quantidade_aulas))

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

    def imprimir_lista_adjacencia(self):
        for vertice in self.vertices:
            retorno = str(vertice.indice) + " =>"
            for adjacente in vertice.adjacentes:
                retorno += " " + str(adjacente.indice)
            print(retorno)

    def imprimir_relatorio(self):
        self.imprimir_preferencias_professores()

    def imprimir_vertices(self):
        for vertice in self.vertices:
            print(vertice)

    def imprimir_horas(self):
        for hora in self.horas:
            print(hora)

    def imprimir_horarios(self):
        for horario in self.horarios:
            print(horario)

    def imprimir_restricoes_professores(self):
        for restricao in self.restricoes_professores:
            print(restricao)

    def imprimir_restricoes_turmas(self):
        for restricao in self.restricoes_turmas:
            print(restricao)

    def imprimir_preferencias_professores(self):
        for preferencia in self.preferencias_professores:
            print(preferencia)

def main():
    grafo1 = Grafo("dados/Escola_A.xlsx")
    grafo2 = Grafo("dados/Escola_B.xlsx")
    grafo3 = Grafo("dados/Escola_C.xlsx")
    grafo4 = Grafo("dados/Escola_D.xlsx")

if __name__ == "__main__":
    main()
