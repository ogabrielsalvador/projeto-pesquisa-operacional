
# LEITURA DO ARQUIVO
def abre_instancia(arq_instancia):
    return linhas


def le_dados_instancia_parametros(arq_instancia):
    return qtde_pontos, qtde_centros, ligacoes_min, ligacoes_max


def le_dados_instancia_coordenadas(arq_instancia):
    return coordenadas


def le_dados_instancia_distancia(arq_instancia):
    return mat_dist


# SEPARAÇÃO DAS COORDENADAS POR QUADRANTES
def tamanho_mapa(arq_instancia):
    return tamanho_x, tamanho_y, min_x, max_x, min_y, max_y


def tamanho_quadrantes(arq_instancia):
    return tam_quad_x, tam_quad_y


def dict_quadrantes_coordenadas(arq_instancia):
    return coordenadas_por_quadrante


# INÍCIO DA HEURÍSTICA
def calcula_m_grande(mat_dist):
    return m_grande


def calcula_distancia(solucao, mat_dist):
    return dist_total, maior_dist


def vmp_inicio(pos_inicio, mat_dist, coordenadas):
    return solucao


def vmp(mat_dist, coordenadas):
    return melhor_solucao, melhor_distancia, maior_distancia


# Salva a solução em um arquivo CSV
def salva_solucao(arq_solucao, solucao, distancia):


# Função que resolve uma instância e salva a solução
def jujuba(arq_instancia, arq_solucao):
