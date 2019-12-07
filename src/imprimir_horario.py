def imprimir_horario(grafo):
    # Dicionario para armazenar as aulas
    aulas = {}
    # Seleciona a turma do primeiro vertice para a impressao
    turma = grafo.vertices[0].turma
    # Seleciona todos os vertices que possuem a mesma turma do primeiro vertice
    for vertice in grafo.vertices:
        if vertice.turma == turma:
            aulas[vertice.cor] = vertice
    # Orneda o diconario pela chave (cor)
    sorted(aulas)
    # Lista para armazenar o horario
    horario = []
    # Calcula a quantidade de aulas por dia
    aulas_por_dia = (len(grafo.horarios) / 5)
    # Contador do loop que forma o horario
    i = 0
    # Loop para formar o horario
    while i < len(grafo.horarios):
        # Se a turma tiver aula nesse horario, adiciona a materia no horario
        if i in aulas:
            horario.append(aulas.get(i).materia)
        # Se a turma nao tiver aula nesse horario, adiciona "-" representando
        # que nao tem aula nesse horario
        else:
            horario.append("-")
        # Incrementa o contator
        i += 1
    # Lista para a impressao da tabela
    table = []
    # Contador do loop que imprime a tabela
    j = 0
    # Loop para imprimir a tabela
    while j < aulas_por_dia:
        # Forma a linha da tabela
        table.append([horario[j], horario[j + int(aulas_por_dia)], horario[j + int(aulas_por_dia * 2)], horario[j + int(aulas_por_dia * 3)], horario[j + int(aulas_por_dia * 4)]])
        # Incrementa o contador do loop da tabela
        j += 1
    # Imprime a tabela
    print(tabulate(table, headers=["Segunda", "Terça", "Quarta", "Quinta", "Sexta"], tablefmt="fancy_grid"))
