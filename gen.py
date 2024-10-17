import numpy as np
import random
import matplotlib.pyplot as plt

# Função para calcular a distância euclidiana
def calcular_distancia(ponto1, ponto2):
    return np.sqrt(np.sum((ponto1 - ponto2) ** 2))

# Função de aptidão: soma total da distância percorrida no ciclo
def aptidao(caminho, pontos):
    distancia_total = 0
    for i in range(len(caminho)):
        distancia_total += calcular_distancia(pontos[caminho[i]], pontos[caminho[(i+1) % len(caminho)]])
    return distancia_total

# Gerar uma população inicial aleatória (população é uma lista de caminhos)
def gerar_populacao(pontos, tamanho_populacao):
    populacao = []
    for _ in range(tamanho_populacao):
        caminho = np.random.permutation(len(pontos))
        populacao.append(caminho)
    return populacao

# Operador de cruzamento (crossover por ordem - OX)
def crossover(pai1, pai2):
    corte1, corte2 = sorted(random.sample(range(len(pai1)), 2))
    filho = [None] * len(pai1)
    filho[corte1:corte2] = pai1[corte1:corte2]
    posicao = corte2
    for gene in pai2:
        if gene not in filho:
            if posicao >= len(pai1):
                posicao = 0
            filho[posicao] = gene
            posicao += 1
    return filho

# Operador de mutação (inversão de duas posições aleatórias)
def mutacao(caminho, taxa_mutacao):
    if random.random() < taxa_mutacao:
        i, j = sorted(random.sample(range(len(caminho)), 2))
        caminho[i:j] = caminho[i:j][::-1]
    return caminho

# Seleção por torneio
def selecao(populacao, pontos, k=3):
    torneio = random.sample(populacao, k)
    torneio.sort(key=lambda individuo: aptidao(individuo, pontos))
    return torneio[0]

# Função principal do algoritmo genético
def algoritmo_genetico(pontos, tamanho_populacao, numero_geracoes, taxa_mutacao):
    # Inicializar a população
    populacao = gerar_populacao(pontos, tamanho_populacao)
    melhor_caminho = None
    melhor_distancia = float('inf')
    historico_aptidao = []

    for geracao in range(numero_geracoes):
        nova_populacao = []
        for _ in range(tamanho_populacao // 2):
            # Seleção de pais
            pai1 = selecao(populacao, pontos)
            pai2 = selecao(populacao, pontos)

            # Cruzamento
            filho1 = crossover(pai1, pai2)
            filho2 = crossover(pai2, pai1)

            # Mutação
            filho1 = mutacao(filho1, taxa_mutacao)
            filho2 = mutacao(filho2, taxa_mutacao)

            nova_populacao.extend([filho1, filho2])

        populacao = nova_populacao

        # Encontrar o melhor indivíduo da geração
        aptidoes = [aptidao(individuo, pontos) for individuo in populacao]
        melhor_aptidao = min(aptidoes)
        melhor_individuo = populacao[np.argmin(aptidoes)]

        if melhor_aptidao < melhor_distancia:
            melhor_distancia = melhor_aptidao
            melhor_caminho = melhor_individuo

        historico_aptidao.append(melhor_distancia)

        # Mostrar o desempenho a cada geração
        if geracao % 10 == 0:
            print(f"Geração {geracao}: Melhor distância = {melhor_distancia}")

    return melhor_caminho, melhor_distancia, historico_aptidao

# Função para visualizar o caminho
def mostrar_caminho(pontos, caminho):
    plt.figure(figsize=(8, 6))
    ciclo = np.append(caminho, caminho[0])  # Fechar o ciclo
    plt.plot(pontos[ciclo, 0], pontos[ciclo, 1], 'o-', markersize=10)
    plt.show()

# Função para gerar pontos aleatórios ou em círculo
def gerar_pontos_uniforme(n):
    return np.random.rand(n, 2) * 100

def gerar_pontos_circulo(n, raio=50):
    angulos = np.linspace(0, 2 * np.pi, n, endpoint=False)
    x = raio * np.cos(angulos) + raio
    y = raio * np.sin(angulos) + raio
    return np.column_stack((x, y))

# Parâmetros do algoritmo genético
tamanho_populacao = 100
numero_geracoes = 500
taxa_mutacao = 0.05

# Teste com pontos aleatórios
pontos_uniformes = gerar_pontos_uniforme(10)
melhor_caminho, melhor_distancia, historico = algoritmo_genetico(pontos_uniformes, tamanho_populacao, numero_geracoes, taxa_mutacao)
mostrar_caminho(pontos_uniformes, melhor_caminho)

# Teste com pontos em círculo
pontos_circulo = gerar_pontos_circulo(10)
melhor_caminho, melhor_distancia, historico = algoritmo_genetico(pontos_circulo, tamanho_populacao, numero_geracoes, taxa_mutacao)
mostrar_caminho(pontos_circulo, melhor_caminho)

# Plotar o desempenho ao longo das gerações
plt.plot(historico)
plt.title("Desempenho ao longo das gerações")
plt.xlabel("Geração")
plt.ylabel("Melhor distância")
plt.show()