import os
from math import sqrt


# LEITURA DO ARQUIVO
def abre_instancia(arq_instancia):
    with open(arq_instancia, "r", encoding="utf8") as f:
        # Lê todas as linhas do arquivo
        linhas = f.readlines()
    return linhas


def le_dados_instancia_parametros(arq_instancia):
    # Lê os dados de um arquivo de instância
    linhas = abre_instancia(arq_instancia)
    # Lê os parâmetros na segunda linha
    qtde_pontos = int(linhas[1].strip().split(";")[0])
    qtde_centros = int(linhas[1].strip().split(";")[1])
    ligacoes_min = int(linhas[1].strip().split(";")[2])
    ligacoes_max = int(linhas[1].strip().split(";")[3])
    return qtde_pontos, qtde_centros, ligacoes_min, ligacoes_max


def le_dados_instancia_coordenadas(arq_instancia):
    # Armazena as coordenadas dos pontos
    coordenadas = list()
    linhas = abre_instancia(arq_instancia)
    qtd_pontos = int(linhas[1].strip().split(";")[0])
    del linhas[:3]
    # Lê as coordenadas
    for i in range(qtd_pontos):
        valores = linhas[i].strip().split(";")
        ponto = int(valores[0])
        x = int(valores[1])
        y = int(valores[2])
        coordenadas.append([x, y, ponto])
    # Retorna os valores lidos
    return coordenadas


def le_dados_instancia_distancia(arq_instancia):
    # Armazena a matriz de distâncias
    mat_dist = list()
    linhas = abre_instancia(arq_instancia)
    qtd_pontos = int(linhas[1].strip().split(";")[0])
    del linhas[:qtd_pontos + 5]
    # Lê a matriz de distâncias
    for i in range(qtd_pontos):
        valores = linhas[i].strip().split(";")
        del valores[0]
        # A linha abaixo usa list comprehension
        # distancias = [int(v) for v in valores]
        # Alternativamente
        distancias = list()
        for v in valores:
            distancias.append(int(v))
        mat_dist.append(distancias)
    return mat_dist


# SEPARAÇÃO DAS COORDENADAS POR QUADRANTES
def tamanho_mapa(arq_instancia):
    lista = le_dados_instancia_coordenadas(arq_instancia)
    lista_x = list()
    lista_y = list()
    # Fazendo a lista do eixo x
    for i in range(len(lista)):
        x = lista[i][0]
        lista_x.append(x)
    lista_x.sort()
    # Fazendo a lista do eixo y
    for i in range(len(lista)):
        y = lista[i][1]
        lista_y.append(y)
    lista_y.sort()

    min_x = lista_x[0]
    max_x = lista_x[len(lista_x) - 1]
    min_y = lista_y[0]
    max_y = lista_y[len(lista_y) - 1]

    tamanho_x = max_x - min_x
    tamanho_y = max_y - min_y
    return tamanho_x, tamanho_y, min_x, max_x, min_y, max_y


def tamanho_quadrantes(arq_instancia):
    tam_x = tamanho_mapa(arq_instancia)[0]
    tam_y = tamanho_mapa(arq_instancia)[1]
    qtde_centros = le_dados_instancia_parametros(arq_instancia)[1]
    resultado_raiz = sqrt(qtde_centros)
    resto = resultado_raiz % 1
    if resto == 0:
        resultado_raiz = int(resultado_raiz)
        tam_quad_x = int(tam_x / resultado_raiz)
        tam_quad_y = int(tam_y / resultado_raiz)
    else:
        tam_quad_x = tam_x
        tam_quad_y = int(tam_y/qtde_centros)
    return tam_quad_x, tam_quad_y


def quadrantes_em_linha(arq_instancia):
    # se o número de quadrantes for primo
    x = arq_instancia
    return x


def quadrantes_em_tabela(arq_instancia):
    x = arq_instancia
    return x


def dict_quadrantes_coordenadas(arq_instancia):
    # Essa def realiza a inclusão de todos os pontos referentes a cada quadrante com base nas coordenas deles.

    tam_quad_x, tam_quad_y = tamanho_quadrantes(arq_instancia)
    tam_x, tam_y, min_x, max_x, min_y, max_y = tamanho_mapa(arq_instancia)
    qtde_pontos, qtde_centros, lig_min, lig_max = le_dados_instancia_parametros(arq_instancia)
    coordenadas = le_dados_instancia_coordenadas(arq_instancia)

    coordenadas_por_quadrante = dict()      # é o dicionário com os pontos de cada quadrante.
    listados = list()                       # é a lista de pontos usados no quadrante atual.

    # CRIAÇÃO DE UMA LISTA ESPELHADA A "coordenadas".
    nao_usados = coordenadas

    # ADICIONANDO OS PONTOS DE CADA QUADRANTE
    if tam_quad_x == tam_x:
        inicio = min_y
        final = min_y + tam_quad_y
        for n in range(1, qtde_centros + 1):    # Irá pegar cada quadrante.
            for i in range(qtde_pontos):
                y = coordenadas[i][1]
                if inicio <= y <= final:
                    listados.append(coordenadas[i])
                    # COMO APAGAR TERMOS DE UMA LISTA ESPELHADA
                    nao_usados = list(filter((coordenadas[i]).__ne__, nao_usados))

            coordenadas = nao_usados
            coordenadas_por_quadrante[n] = listados
            listados = list()

            inicio += tam_quad_y
            final += tam_quad_y
    else:
        coordenadas_por_quadrante['Não Feito'] = 'dividir diferente'

    return coordenadas_por_quadrante


# INÍCIO DA HEURÍSTICA
def calcula_m_grande(mat_dist):
    m_grande = 0

    for linha in mat_dist:
        maior_valor_linha = max(linha)
        if maior_valor_linha > m_grande:
            m_grande = maior_valor_linha
    m_grande += 1

    # Retorna o M grande
    return m_grande


def calcula_distancia(solucao, mat_dist):
    # Calcula a distância total de uma dada solução
    dist_total = 0
    maior_dist = 0      # maior distância entre dois pontos
    qtde_pontos = len(solucao)

    # Soma todas as distâncias para percorrer todos os pontos
    for i in range(1, qtde_pontos):
        de = solucao[i - 1]
        para = solucao[i]
        dist_total += mat_dist[de][para]

        if mat_dist[de][para] > maior_dist:
            maior_dist = mat_dist[de][para]

    # Falta somar a distância de retorno para a origem
    de = solucao[-1]
    para = solucao[0]
    dist_total += mat_dist[de][para]

    # Retorna a distância total
    return dist_total, maior_dist


def vmp_inicio(pos_inicio, mat_dist, coordenadas):
    # Aplica o algoritmo VMP para um início específico
    # Faz uma cópia da matriz
    distancias = [linha.copy() for linha in mat_dist]

    # Constrói a solução inicial
    ponto_inicio = coordenadas[pos_inicio][2]
    solucao = [ponto_inicio]
    pos_ultimo_adicionado = pos_inicio        # posição na lista de coordenadas
    ponto_ultimo_adicionado = coordenadas[pos_ultimo_adicionado][2]     # refere-se ao id do ponto

    # Coloca o M grande na coluna do ponto de início
    tam_mat = len(distancias)
    m_grande = calcula_m_grande(mat_dist)
    for i in range(tam_mat):
        distancias[i][ponto_ultimo_adicionado] = m_grande

    # Constrói o restante da solução
    tam_coord = len(coordenadas)
    for _ in range(tam_coord - 1):

        # Calculando a mínima distância:
        min_dist = 9999
        for n in range(0, tam_coord):
            para = coordenadas[n][2]
            dist_atual = distancias[ponto_ultimo_adicionado][para]
            if dist_atual < min_dist:
                min_dist = dist_atual

        ponto_min_dist = distancias[ponto_ultimo_adicionado].index(min_dist)

        solucao.append(ponto_min_dist)
        ponto_ultimo_adicionado = ponto_min_dist

        # Coloca o M grande na coluna do último ponto adicionado
        for i in range(tam_mat):
            distancias[i][ponto_ultimo_adicionado] = m_grande

    # Retorna a solução encontrada
    return solucao


def vmp(mat_dist, coordenadas):
    # Resolve o VMP para todos os inícios possíveis
    # Armazena a melhor solucao de todas
    melhor_solucao = None
    melhor_distancia = float("inf")
    maior_distancia = float("inf")

    # Para cada início, chama o vmp_inicio
    qtde_pontos = len(coordenadas)
    for pos_inicio in range(qtde_pontos):
        solucao_inicio = vmp_inicio(pos_inicio, mat_dist, coordenadas)
        solucao_inicio_valor, maior_dist = calcula_distancia(solucao_inicio, mat_dist)

        # Testa se é a melhor solução de todas
        if solucao_inicio_valor < melhor_distancia:
            melhor_solucao = solucao_inicio
            melhor_distancia = solucao_inicio_valor
            maior_distancia = maior_dist

    # Retorna a melhor solução de todas e o seu valor
    return melhor_solucao, melhor_distancia, maior_distancia


# Salva a solução em um arquivo CSV
def salva_solucao(arq_solucao, solucao, distancia):
    with open(arq_solucao, "w+", encoding="utf8") as f:
        f.write(f"{distancia}\n")
        # Escreve até o penúltimo ponto, com ";"
        for ponto in solucao[:-1]:
            f.write(f"{ponto};")
        # Escreve o último ponto
        f.write(f"{solucao[-1]}")


# Função que resolve uma instância e salva a solução
def jujuba(arq_instancia, arq_solucao):
    # Lê os dados da instância
    qtde_quadrantes = le_dados_instancia_parametros(arq_instancia)[1]
    coordenadas_por_quadrante = dict_quadrantes_coordenadas(arq_instancia)
    mat_dist = le_dados_instancia_distancia(arq_instancia)

    solucao = list()

    # Separando por quadrantes
    dist_total = 0
    maior_distancia = 0
    for n in range(1, qtde_quadrantes + 1):

        # Aplica o algoritmo VMP para obter a solução de cada quadrante
        coordenadas = coordenadas_por_quadrante[n]
        solucao_quad, dist_total_quad, maior_dist_quad = vmp(mat_dist, coordenadas)
        solucao.append(solucao_quad)    # solucao geral da instancia
        dist_total += dist_total_quad   # distancia total da instancia

        """
        print(f'As coordenadas do quadrante {n} são \n{coordenadas}\n')
        print(f'A MELHOR solução do quadrante {n} é {solucao_quad}\n')
        print(f'A MAIOR distancia entre dois pontos no quadrante {n} é {maior_dist_quad}\n')
        print(f'A MENOR distancia total do quadrante {n} é {dist_total_quad}')
        print('-' * 50)
        """

        if maior_dist_quad > maior_distancia:
            maior_distancia = maior_dist_quad

    print(f'A MAIOR distancia entre dois pontos na instância é {maior_distancia}\n')
    """
    print(f'A MENOR distancia total da instância é {dist_total}')
    print('=' * 50)
    """

    # Salva a solução no arquivo CSV
    salva_solucao(arq_solucao, solucao, dist_total)


# Procedimento principal
def main():
    pasta_instancias = 'instancias'
    pasta_solucoes = 'Solucoes_Teste'
    lista_arquivos = os.listdir(pasta_instancias)
    lista_arquivos.sort()
    for arquivo in lista_arquivos:
        arq_instancia = os.path.join(pasta_instancias, arquivo)
        arq_solucao = os.path.join(pasta_solucoes, arquivo)
        jujuba(arq_instancia, arq_solucao)

if __name__ == "__main__":
    main()