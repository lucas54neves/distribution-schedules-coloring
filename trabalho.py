import xlrd

# Classe que representa os vertices
class Vertice:
    def __init__(self, materia, turma, professor, quantidade_aulas):
        self.materia = materia
        self.turma = turma
        self.professor = professor
        self.quantidade_aulas = quantidade_aulas

    def imprimir(self):
        print(self.materia, self.turma, self.professor, self.quantidade_aulas)

# Classe que representa o grafo
class Grafo:
    def __init__(self):
        self.lista_vertices = []

    def adicionar_vertices(self, materia, turma, professor, quantidade_aulas):
        self.lista_vertices.append(Vertice(materia, turma, professor, quantidade_aulas))

    def imprimir(self):
        for vertice in self.lista_vertices:
            vertice.imprimir()

# Funcao para leitura da planilha
def leitura(nome_arquivo):
    # Abre o arquivo
    planilha = xlrd.open_workbook(nome_arquivo)
    # Pega a primeira aba da planilha, a aba Dados
    aba = planilha.sheets()[0]
    # Grafo para retornar
    grafo = Grafo()

    # Loop para leitura dos dados
    for i in xrange(aba.nrows):
        if i != 0:
            valores = aba.row_values(i)
            grafo.adicionar_vertices(str(valores[0]), int(valores[1]), str(valores[2]), int(valores[3]))

    grafo.imprimir()
    
    # Retorna o grafo criado com os dados da planilha
    return grafo

leitura("dados/Escola_A.xlsx")
