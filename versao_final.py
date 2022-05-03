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

    # Analisando se o número de centros é primo
    # Se SIM, os quadrantes serão em LINHAS
    # Se NÃO, os quadrantes serão em TABELAS
    if qtde_centros > 1:
        for i in range(2, int(qtde_centros / 2) + 1):
            if qtde_centros % i == 0:
                primo = False
                break
        else:
            primo = True
    else:
        primo = False

    # Analisando se o número de centros possui raíz quadrada inteira e qual o múltiplo do número de centros
    # Se SIM, os quadrantes terão as dimensões de quadrados
    # Se NÃO, os quadrantes terão as dimensões de retângulos
    resultado_raiz = sqrt(qtde_centros)
    if resultado_raiz % 1 == 0:
        multiplo = int(resultado_raiz)
    else:
        multiplo = 1
        for i in range(2, 6):
            if qtde_centros % i == 0:
                multiplo = i

    # Dimensões dos quadrantes em linha
    if primo:
        tam_quad_x = tam_x
        tam_quad_y = tam_y / qtde_centros

    # Dimensões dos quadrantes em tabela / quadrados e retângulos
    else:
        tam_quad_x = tam_x / multiplo
        tam_quad_y = tam_y / (qtde_centros / multiplo)

    return tam_quad_x, tam_quad_y, primo, multiplo


def ponto_central_quadrante(arq_instancia):
    # Definindo o centro de cada quadrante
    qtde_centros = le_dados_instancia_parametros(arq_instancia)[1]
    tam_quad_x, tam_quad_y, primo, colunas = tamanho_quadrantes(arq_instancia)
    linhas = int(qtde_centros / colunas)
    min_x = tamanho_mapa(arq_instancia)[2]
    min_y = tamanho_mapa(arq_instancia)[4]

    lista = list()      # é uma lista dos pontos centrais de cada quadrante

    if primo:
        centro_x = tam_quad_x / 2       # o meio em X
        for i in range(qtde_centros):
            inicio_y = min_y + (tam_quad_y * i)
            centro_y = inicio_y + (tam_quad_y / 2)      # o meio em Y
            lista.append([centro_x, centro_y])

    else:
        for line in range(linhas):
            inicio_y = min_y + (tam_quad_y * line)
            centro_y = inicio_y + (tam_quad_y / 2)
            for column in range(colunas):
                inicio_x = min_x + (tam_quad_x * column)
                centro_x = inicio_x + (tam_quad_x / 2)
                lista.append([centro_x, centro_y])

    # Retorna a lista dos pontos centrais de cada quadrante
    return lista


def dict_quadrantes_coordenadas_provisorio(arq_instancia):
    # Essa def realiza a inclusão de todos os pontos referentes a cada quadrante com base nas coordenas deles.

    tam_quad_x, tam_quad_y, primo, multiplo = tamanho_quadrantes(arq_instancia)
    min_x = tamanho_mapa(arq_instancia)[2]
    min_y = tamanho_mapa(arq_instancia)[4]
    qtde_centros = le_dados_instancia_parametros(arq_instancia)[1]

    coordenadas = le_dados_instancia_coordenadas(arq_instancia)
    coordenadas_por_quadrante = dict()  # é o dicionário dos pontos de cada quadrante.

    listados = list()  # é a lista de pontos usados no quadrante atual.

    # CRIAÇÃO DE UMA LISTA ESPELHADA A "coordenadas".
    nao_usados = coordenadas

    # ADICIONANDO OS PONTOS DE CADA QUADRANTE
    inicio_y = min_y
    final_y = min_y + tam_quad_y

    # ADICIONANDO OS PONTOS DAS INSTÂNCIAS COM QUADRANTES EM LINHA
    if primo:
        for n in range(1, qtde_centros + 1):  # Irá pegar cada quadrante.
            for i in range(len(coordenadas)):  # Irá passar por todos os pontos
                y = coordenadas[i][1]
                if inicio_y <= y <= final_y:
                    listados.append(coordenadas[i])

                    # COMO APAGAR TERMOS DE UMA LISTA ESPELHADA
                    nao_usados = list(filter((coordenadas[i]).__ne__, nao_usados))

            coordenadas = nao_usados
            coordenadas_por_quadrante[n] = sorted(listados)
            listados = list()

            inicio_y += tam_quad_y
            final_y += tam_quad_y + 1

    # ADICIONANDO OS PONTOS DAS INSTÂNCIAS COM QUADRANTES EM TABELA
    else:

        # CRIAÇÃO DE UMA LISTA REFERENTES A LINHA.
        linha = list()
        c = 0

        for n in range(int(qtde_centros / multiplo)):  # Irá pegar todos os pontos da linha.
            for m in range(multiplo):
                c += 1      # Refere-se ao número do quadrante.
                for i in range(len(coordenadas)):  # Irá passar por todos os pontos da instância.
                    y = coordenadas[i][1]
                    if inicio_y <= y <= final_y:
                        linha.append(coordenadas[i])

                inicio_x = min_x + (tam_quad_x * m)
                final_x = inicio_x + tam_quad_x

                for i in range(len(linha)):
                    x = linha[i][0]
                    if inicio_x <= x <= final_x:
                        listados.append(linha[i])

                        # Apagando os pontos usados da lista 'linha'
                        nao_usados = list(filter((linha[i]).__ne__, nao_usados))

                # Somando os inícios e finais de y, para passarmos p/ próxima linha
                if m == (multiplo - 1):
                    inicio_y += tam_quad_y
                    final_y += tam_quad_y + 1

                coordenadas = nao_usados
                coordenadas_por_quadrante[c] = sorted(listados)
                listados = list()
                linha = list()

    return coordenadas_por_quadrante


def calcula_distancia(ponto_1, ponto_2):
    # calcula a distância com base nos dois pontos informados
    x1 = ponto_1[0]
    x2 = ponto_2[0]
    y1 = ponto_1[1]
    y2 = ponto_2[1]

    if x1 == x2 and y1 == y2:
        distancia = 0

    else:
        dif_x = x1 - x2
        if dif_x < 0:
            dif_x *= -1

        dif_y = y1 - y2
        if dif_y < 0:
            dif_y *= -1

        distancia = sqrt((dif_x ** 2) + (dif_y ** 2))

    # Retorna a distancia entre dois pontos
    return distancia


def dict_quadrantes_coordenadas_sem_centro(arq_instancia):
    # faz os quadrantes respeitarem a qtde min e max de lig dos pts ao centro
    coordenadas_por_quadrante = dict_quadrantes_coordenadas_provisorio(arq_instancia)
    pontos_total, qtde_centros, lig_min, lig_max = le_dados_instancia_parametros(arq_instancia)
    pontos_centrais = ponto_central_quadrante(arq_instancia)

    nao_usados = list()  # lista dos pontos que não estão vinculados a algum quadrante

    # tratando cada quadrante por vez
    for i in range(1, qtde_centros + 1):

        # respeitando o número máximo de ligações
        while True:
            qtde_pontos_quad = len(coordenadas_por_quadrante[i])
            if qtde_pontos_quad <= lig_max:
                break
            else:
                nao_usados.append(coordenadas_por_quadrante[i][-1])
                nao_usados = sorted(nao_usados)
                del coordenadas_por_quadrante[i][-1]

        # respeitando o número mínimo de ligações
        while True:
            qtde_pontos_quad = len(coordenadas_por_quadrante[i])
            if qtde_pontos_quad >= lig_min + 1:
                break

            else:
                qtde_livre = len(nao_usados)
                centro = pontos_centrais[i - 1]
                menor_dist = float('inf')
                pos_ponto_mais_perto = None

                if qtde_livre > 0:  # irá pegar os pontos livres
                    for pos_ponto in range(qtde_livre):     # loop para descobrir o ponto mais próximo
                        ponto = nao_usados[pos_ponto]
                        distancia = calcula_distancia(centro, ponto)
                        if distancia < menor_dist:
                            menor_dist = distancia
                            pos_ponto_mais_perto = pos_ponto
                    coordenadas_por_quadrante[i].append(nao_usados[pos_ponto_mais_perto])
                    coordenadas_por_quadrante[i] = sorted(coordenadas_por_quadrante[i])
                    del nao_usados[pos_ponto_mais_perto]

                else:  # irá pegar do quad que tiver mais pontos
                    maior_quad_pts = 0      # qtde de pts no quadrante com mais pts
                    n_quad = None       # qual o quadrante que possui mais pts
                    for c in range(1, qtde_centros + 1):        # loop para descobrir o quadrante com mais pontos
                        tam_quad_pts = len(coordenadas_por_quadrante[c])
                        if tam_quad_pts > maior_quad_pts:
                            maior_quad_pts = tam_quad_pts       # qtde de pts no quadrante com mais pts
                            n_quad = c                          # qual o quadrante que possui mais pts
                    for pos_ponto in range(maior_quad_pts):     # loop para descobrir o ponto mais próximo
                        ponto = coordenadas_por_quadrante[n_quad][pos_ponto]
                        distancia = calcula_distancia(centro, ponto)
                        if distancia < menor_dist:
                            menor_dist = distancia
                            pos_ponto_mais_perto = pos_ponto
                    coordenadas_por_quadrante[i].append(coordenadas_por_quadrante[n_quad][pos_ponto_mais_perto])
                    coordenadas_por_quadrante[i] = sorted(coordenadas_por_quadrante[i])
                    del coordenadas_por_quadrante[n_quad][pos_ponto_mais_perto]

    # garantindo que não terá pontos livres
    while True:
        qtde_livre = len(nao_usados)
        menor_dist = float('inf')
        pos_ponto_mais_perto = None

        if qtde_livre == 0:
            break

        else:  # irá adicionar ao quadrante que tiver menos pontos
            menor_quad_pts = float('inf')
            n_quad = None
            for c in range(1, qtde_centros + 1):  # loop para descobrir o quadrante com menos pontos
                tam_quad_pts = len(coordenadas_por_quadrante[c])
                if tam_quad_pts < menor_quad_pts:
                    menor_quad_pts = tam_quad_pts
                    n_quad = c

            centro = pontos_centrais[n_quad - 1]
            for pos_ponto in range(qtde_livre):  # loop para descobrir o ponto não usado mais próximo
                ponto = nao_usados[pos_ponto]
                distancia = calcula_distancia(centro, ponto)
                if distancia < menor_dist:
                    menor_dist = distancia
                    pos_ponto_mais_perto = pos_ponto

            coordenadas_por_quadrante[n_quad].append(nao_usados[pos_ponto_mais_perto])
            coordenadas_por_quadrante[n_quad] = sorted(coordenadas_por_quadrante[n_quad])
            del nao_usados[pos_ponto_mais_perto]

    return coordenadas_por_quadrante


def dict_quadrantes_coordenadas(arq_instancia):
    coordenadas_por_quadrante = dict_quadrantes_coordenadas_sem_centro(arq_instancia)
    centros_dos_quadrantes = ponto_central_quadrante(arq_instancia)
    qtde_centros = len(coordenadas_por_quadrante)

    for quad in range(1, qtde_centros + 1):        # irá passar por todos os quadrantes de cada vez
        solucao = coordenadas_por_quadrante[quad]
        centro_quad = centros_dos_quadrantes[quad - 1]
        centro_quad_y = centro_quad[1]
        centro_ideal = (500, 500)
        centro_ideal_y = 500

        menor_dist = float("inf")
        ponto_central = None
        pos_ponto_central = None

        if centro_quad_y < centro_ideal_y:      # o quadrante fica pra cima da metade
            for pos_ponto in range(len(solucao)):      # irá passar por todos os pontos do quadrante
                ponto = solucao[pos_ponto]
                ponto_y = ponto[1]

                if ponto_y < centro_ideal_y:    # o ponto precisa estar pra cima da metade
                    distancia = calcula_distancia(ponto, centro_ideal)
                    if distancia < menor_dist:      # irá buscar pelo ponto mais próximo ao centro ideal
                        menor_dist = distancia
                        ponto_central = ponto
                        pos_ponto_central = pos_ponto

        else:       # o quadrante fica pra baixo da metade
            for pos_ponto in range(len(solucao)):   # irá passar por todos os pontos do quadrante
                ponto = solucao[pos_ponto]
                ponto_y = ponto[1]

                if ponto_y > centro_ideal_y:        # o ponto precisa estar pra baixo da metade
                    distancia = calcula_distancia(ponto, centro_ideal)
                    if distancia < menor_dist:      # irá buscar pelo ponto mais próximo ao centro ideal
                        menor_dist = distancia
                        ponto_central = ponto
                        pos_ponto_central = pos_ponto

        del solucao[pos_ponto_central]              # apagando o ponto central da solução
        solucao.insert(0, ponto_central)            # e adicionando ele a primeira posição da solução
        coordenadas_por_quadrante[quad] = solucao   # colocando a solução (com o centro em primeiro) no seu quadrante

    # Retorna um dicionário com as coordenadas de cada quadrante e o seu centro estando em primeiro
    return coordenadas_por_quadrante


# SALVANDO A SOLUÇÃO EM UM ARQUIVO CSV
def salva_solucao(arq_solucao, solucao, distancia):
    with open(arq_solucao, "w+", encoding="utf8") as f:
        f.write(f"{distancia}\n")

        qtde_quad = len(solucao)
        for quad in range(0, qtde_quad):

            # Escreve até o penúltimo ponto, com ";"
            qtde_pts = len(solucao[quad])
            for i in range(qtde_pts - 1):
                ponto = solucao[quad][i]
                f.write(f"{ponto};")

            # Escreve o último ponto
            if quad != qtde_quad - 1:
                f.write(f"{solucao[quad][-1]}\n")
            else:
                f.write(f"{solucao[quad][-1]}")


# RESOLVENDO A INSTÂNCIA
def resolve_instancia(arq_instancia, arq_solucao):
    # Lê os dados da instância
    qtde_quadrantes = le_dados_instancia_parametros(arq_instancia)[1]
    coordenadas_por_quadrante = dict_quadrantes_coordenadas(arq_instancia)
    mat_dist = le_dados_instancia_distancia(arq_instancia)

    solucao = list()
    solucao_quad = list()
    maior_distancia = 0

    # Separando por quadrantes
    for quad in range(1, qtde_quadrantes + 1):      # irá passar por todos os quadrantes
        qtde_pontos = len(coordenadas_por_quadrante[quad])      # qtde de pts do quadrante atual
        ponto_central = coordenadas_por_quadrante[quad][0][2]
        solucao_quad.append(ponto_central)      # adicionando o ponto central do quadrante na primeira posição
        de = ponto_central

        for pos_ponto in range(1, qtde_pontos):     # irá passar por todos os pts do quadrante, exceto o primeiro (central)
            ponto = coordenadas_por_quadrante[quad][pos_ponto][2]
            solucao_quad.append(ponto)
            para = ponto
            distancia = mat_dist[de][para]

            if distancia > maior_distancia:     # buscando a maior distância entre o centro e algum ponto
                maior_distancia = distancia

        solucao.append(solucao_quad)
        solucao_quad = list()

    # Salva a solução no arquivo CSV
    salva_solucao(arq_solucao, solucao, maior_distancia)


# Procedimento principal
def main():
    pasta_instancias = 'instancias'
    pasta_solucoes = 'Solucoes_Teste'
    lista_arquivos = os.listdir(pasta_instancias)
    lista_arquivos.sort()
    for arquivo in lista_arquivos:
        arq_instancia = os.path.join(pasta_instancias, arquivo)
        arq_solucao = os.path.join(pasta_solucoes, arquivo)
        resolve_instancia(arq_instancia, arq_solucao)


if __name__ == "__main__":
    main()
