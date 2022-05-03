import os


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

    tam_quad_x = tam_x
    tam_quad_y = tam_y / qtde_centros

    return tam_quad_x, tam_quad_y


def dict_quadrantes_coordenadas_provisorio(arq_instancia):
    # Essa def realiza a inclusão de todos os pontos referentes a cada quadrante com base nas coordenas deles.

    tam_quad_y = tamanho_quadrantes(arq_instancia)[1]
    min_y = tamanho_mapa(arq_instancia)[4]
    qtde_centros = le_dados_instancia_parametros(arq_instancia)[1]

    coordenadas = le_dados_instancia_coordenadas(arq_instancia)
    coordenadas_por_quadrante = dict()  # é o dicionário dos pontos de cada quadrante.
    listados = list()  # é a lista de pontos usados no quadrante atual.

    # CRIAÇÃO DE UMA LISTA ESPELHADA A "coordenadas".
    nao_usados = coordenadas

    # ADICIONANDO OS PONTOS DE CADA QUADRANTE
    inicio = min_y
    final = min_y + tam_quad_y
    for n in range(1, qtde_centros + 1):  # Irá pegar cada quadrante.
        for i in range(len(coordenadas)):  # Irá passar por todos os pontos
            y = coordenadas[i][1]
            if inicio <= y <= final:
                listados.append(coordenadas[i])

                # COMO APAGAR TERMOS DE UMA LISTA ESPELHADA
                nao_usados = list(filter((coordenadas[i]).__ne__, nao_usados))

        coordenadas = nao_usados
        coordenadas_por_quadrante[n] = sorted(listados)
        listados = list()

        inicio += tam_quad_y
        final += tam_quad_y + 1

    return coordenadas_por_quadrante


def dict_quadrantes_coordenadas(arq_instancia):
    coordenadas_por_quadrante = dict_quadrantes_coordenadas_provisorio(arq_instancia)
    pontos_total, qtde_centros, lig_min, lig_max = le_dados_instancia_parametros(arq_instancia)

    nao_usados = list()  # lista dos pontos que não estão vinculados a algum ponto

    # tratando cada quadrante por vez
    for i in range(1, qtde_centros + 1):

        # respeitando o número máximo de ligações
        while True:
            qtde_pontos_quad = len(coordenadas_por_quadrante[i])
            if qtde_pontos_quad <= lig_max:
                break
            else:
                nao_usados.append(coordenadas_por_quadrante[i][qtde_pontos_quad - 1])
                sorted(nao_usados)
                del coordenadas_por_quadrante[i][qtde_pontos_quad - 1]

        # respeitando o número mínimo de ligações
        while True:
            qtde_pontos_quad = len(coordenadas_por_quadrante[i])
            if qtde_pontos_quad >= lig_min:
                break
            else:
                qtde_livre = len(nao_usados)
                if qtde_livre > 0:  # irá pegar os pontos livres
                    coordenadas_por_quadrante[i].append(nao_usados[qtde_livre - 1])
                    sorted(coordenadas_por_quadrante[i])
                    del nao_usados[qtde_livre - 1]
                else:  # irá pegar do quad que tiver mais pontos
                    maior_quad = 0
                    n_quad = None
                    for c in range(1, qtde_centros + 1):  # loop para descobrir o quadrante com mais pontos
                        tam_quad = len(coordenadas_por_quadrante[c])
                        if tam_quad > maior_quad:
                            maior_quad = tam_quad
                            n_quad = c
                    coordenadas_por_quadrante[i].append(coordenadas_por_quadrante[n_quad][maior_quad - 1])
                    sorted(coordenadas_por_quadrante[i])
                    del coordenadas_por_quadrante[n_quad][maior_quad - 1]

    # garantindo que não terá pontos livres
    while True:
        qtde_livre = len(nao_usados)
        if qtde_livre == 0:
            break
        else:  # irá adicionar ao quadrante que tiver menos pontos
            menor_quad = 9999
            n_quad = None
            for c in range(1, qtde_centros + 1):  # loop para descobrir o quadrante com menos pontos
                tam_quad = len(coordenadas_por_quadrante[c])
                if tam_quad < menor_quad:
                    menor_quad = tam_quad
                    n_quad = c
            coordenadas_por_quadrante[n_quad].append(nao_usados[qtde_livre - 1])
            sorted(coordenadas_por_quadrante[n_quad])
            del nao_usados[qtde_livre - 1]

    return coordenadas_por_quadrante


# INÍCIO DOS CÁLCULOS
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
    maior_dist = 0  # maior distância entre dois pontos
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

    # Retorna a distância total e maior distância entre dois pontos na dada solução
    return dist_total, maior_dist


def vmp_inicio(pos_inicio, mat_dist, coordenadas):
    # Aplica o algoritmo VMP para um início específico
    # Faz uma cópia da matriz
    distancias = [linha.copy() for linha in mat_dist]

    # Constrói a solução inicial
    ponto_inicio = coordenadas[pos_inicio][2]
    solucao = [ponto_inicio]
    pos_ultimo_adicionado = pos_inicio  # posição na lista de coordenadas
    ponto_ultimo_adicionado = coordenadas[pos_ultimo_adicionado][2]  # refere-se ao id do ponto

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
        if maior_dist < maior_distancia:
            melhor_solucao = solucao_inicio
            melhor_distancia = solucao_inicio_valor
            maior_distancia = maior_dist

    # Retorna a melhor solução de todas e o seu valor
    return melhor_solucao, melhor_distancia, maior_distancia


# Salva a solução em um arquivo CSV
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
            f.write(f"{solucao[quad][-1]}\n")
            f.write(f'')


# Função que resolve uma instância e salva a solução
def resolve_instancia(arq_instancia, arq_solucao):
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
        solucao.append(solucao_quad)  # solucao geral da instancia
        dist_total += dist_total_quad  # distancia total da instancia

        if maior_dist_quad > maior_distancia:
            maior_distancia = maior_dist_quad

    # Salva a solução no arquivo CSV
    salva_solucao(arq_solucao, solucao, maior_distancia)
    return solucao, maior_distancia


# def para corrigir o resultado
def correcao(arq_instancia, arq_solucao):
    # GABARITO
    qtde_pontos_gab, qtde_centros_gab, lig_min_gab, lig_max_gab = le_dados_instancia_parametros(arq_instancia)

    dict_distancia_gab = {'01': 420, '02': 433, '03': 344, '04': 372, '05': 329,
                          '06': 288, '07': 338, '08': 355, '09': 302, '10': 337,
                          '11': 266, '12': 304, '13': 315, '14': 281, '15': 315,
                          '16': 236, '17': 291, '18': 217, '19': 229, '20': 278,
                          '21': 294, '22': 297, '23': 285, '24': 293, '25': 282,
                          '26': 213, '27': 204, '28': 211, '29': 208, '30': 209,
                          '31': 482, '32': 436, '33': 648, '34': 614, '35': 597,
                          '36': 653, '37': 473, '38': 544, '39': 527, '40': 711,
                          '41': 327, '42': 452, '43': 634, '44': 444, '45': 679,
                          '46': 665, '47': 519, '48': 472, '49': 673, '50': 659,
                          '51': 317, '52': 534, '53': 329, '54': 330, '55': 598,
                          '56': 359, '57': 303, '58': 645, '59': 506, '60': 657}
    n_instancia = arq_instancia[16:18]
    maior_dist_gab = dict_distancia_gab[n_instancia]

    # MEU RESULTADO
    maior_dist_sol = resolve_instancia(arq_instancia, arq_solucao)[1]
    """
    # INÍCIO DA CORREÇÃO
    print(f'\033[7;97;107m{" " * 65}\033[m')
    print(f'\033[7;97;41m{"Correção da instância " + arq_instancia[16:18]:^65}\033[m')
    print(f'\033[7;97;107m{" " * 65}\033[m\n')

    # Corrigindo o número de centros
    qtde_centros_sol = len(solucao)
    if qtde_centros_sol == qtde_centros_gab:
        print(f'\033[1;32mCORRETO!\033[m A quantidade de centros deve ser \033[1;34m{qtde_centros_gab}\033[m.\n'
              f'A solução teve \033[1;32m{qtde_centros_sol}\033[m centros.\n')
    else:
        print(f'\033[1;31mERRO!\033[m O número de centros deve ser: \033[1;34m{qtde_centros_gab}\033[m.\n'
              f'Mas a solução possui \033[1;31m{qtde_centros_sol}\033[m.\n')

    # Corrigindo minimo e maximo
    for i in range(qtde_centros_sol):
        qtde_pontos_quad = len(solucao[i])
        qtde_pontos_sol += qtde_pontos_quad
        if lig_min_gab <= qtde_pontos_quad <= lig_max_gab:
            print(f'\033[1;32mCORRETO!\033[m A quantidade de mínima deve ser \033[1;34m{lig_min_gab}\033[m e máxima deve ser \033[1;34m{lig_max_gab}\033[m.\n'
                  f'O quadrante \033[1;37m{i + 1}\033[m teve \033[1;32m{qtde_pontos_quad}\033[m pontos.\n')
        elif lig_max_gab < qtde_pontos_quad:
            print(f'\033[1;31mERRO!\033[m O número máximo de pontos por quadrante deve ser: \033[1;34m{lig_max_gab}\n'
                  f'Mas o quadrante \033[1;34m{i + 1}\033[m possui \033[1;32m{qtde_pontos_quad}\033[m\n')
        else:
            print(f'\033[1;31mERRO!\033[m O número mínimo de pontos por quadrante deve ser: \033[1;34m{lig_min_gab}\033[m\n'
                  f'Mas o quadrante \033[1;34m{i + 1}\033[m possui \033[1;32m{qtde_pontos_quad}\033[m\n')

    # Corrigindo o número de pontos
    if qtde_pontos_sol == qtde_pontos_gab:
        print(f'\033[1;32mCORRETO!\033[m A quantidade de pontos deve ser \033[1;34m{qtde_pontos_gab}\033[m.\n'
              f'A solução teve \033[1;32m{qtde_pontos_sol}\033[m pontos.\n')
    else:
        print(f'\033[1;31mERRO!\033[m O número de pontos deve ser: \033[1;34m{qtde_pontos_gab}\033[m.\n'
              f'Mas a solução possui \033[1;31m{qtde_pontos_sol}\033[m.\n')
    """
    # Verificando o GAP da distância
    gap = int(((maior_dist_sol / maior_dist_gab) - 1) * 100)
    if gap <= 20:
        print(f'\033[1;32m{gap}\033[m')
    elif gap <= 50:
        print(f'\033[1;34m{gap}\033[m')
    elif gap <= 100:
        print(f'\033[1;35m{gap}\033[m')
    elif gap <= 200:
        print(f'\033[1;33m{gap}\033[m')
    else:
        print(f'\033[1;31m{gap}\033[m')
    """
    # FIM DA CORREÇÃO
    print(f'{"=" * 65}')
    """


# Procedimento principal
def main():
    pasta_instancias = 'instancias'
    pasta_solucoes = 'Solucoes_Teste'
    lista_arquivos = os.listdir(pasta_instancias)
    lista_arquivos.sort()
    for arquivo in lista_arquivos:
        arq_instancia = os.path.join(pasta_instancias, arquivo)
        arq_solucao = os.path.join(pasta_solucoes, arquivo)
        correcao(arq_instancia, arq_solucao)


if __name__ == "__main__":
    main()
