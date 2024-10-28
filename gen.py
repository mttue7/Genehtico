import numpy as np
import random
import matplotlib.pyplot as plt
import time

# Função para calcular a distância euclidiana entre dois pontos
def calcular_distancia(ponto1, ponto2):
    return np.sqrt(np.sum((ponto1 - ponto2) ** 2))

# Função de aptidão: calcula a soma total da distância percorrida no ciclo
def aptidao(caminho, pontos):
    distancia_total = 0
    for i in range(len(caminho)):
        distancia_total += calcular_distancia(pontos[caminho[i]], pontos[caminho[(i + 1) % len(caminho)]])
    return distancia_total

# Geração inicial de população aleatória (população é uma lista de caminhos)
def gerar_populacao(pontos, tamanho_populacao):
    populacao = []
    for _ in range(tamanho_populacao):
        caminho = np.random.permutation(len(pontos))  # Gera um caminho aleatório
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

# Seleção por torneio, com tamanho de torneio k
def selecao(populacao, pontos, k=3):
    torneio = random.sample(populacao, k)
    torneio.sort(key=lambda individuo: aptidao(individuo, pontos))
    return torneio[0]

# Função principal do algoritmo genético
def algoritmo_genetico(pontos, tamanho_populacao, numero_geracoes, taxa_mutacao):
    # Inicializa a população com caminhos aleatórios
    populacao = gerar_populacao(pontos, tamanho_populacao)
    melhor_caminho = None
    melhor_distancia = float('inf')
    historico_aptidao = []  # Histórico para acompanhar o desempenho

    # Variáveis para critério de parada
    repeticoes_consecutivas = 0
    gen_Inicio = None
    ultima_aptidao = None

    # Loop principal do algoritmo genético
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

        # Encontrar o melhor indivíduo da geração atual
        aptidoes = [aptidao(individuo, pontos) for individuo in populacao]
        melhor_aptidao = min(aptidoes)
        melhor_individuo = populacao[np.argmin(aptidoes)]

        # Verificação de repetição da melhor aptidão
        if melhor_aptidao == ultima_aptidao:
            repeticoes_consecutivas += 1
            if repeticoes_consecutivas == 1:
                gen_Inicio = geracao
        else:
            repeticoes_consecutivas = 0
            gen_Inicio = None

        ultima_aptidao = melhor_aptidao

        # Critério de parada: 80 gerações consecutivas com a mesma aptidão
        if repeticoes_consecutivas >= 80 and gen_Inicio is not None:
            print("Critério de parada atingido: Melhor aptidão repetida por 80 gerações")
            break

        # Atualizar o melhor caminho encontrado
        if melhor_aptidao < melhor_distancia:
            melhor_distancia = melhor_aptidao
            melhor_caminho = melhor_individuo

        # Salvar histórico de aptidão
        historico_aptidao.append(melhor_distancia)

        # Mostrar o desempenho a cada geração
        print(f"Geração {geracao}: Melhor distância = {melhor_distancia:.3f}")

    return melhor_caminho, melhor_distancia, historico_aptidao

# Função para visualizar o caminho gerado
def mostrar_caminho(pontos, caminho, ax):
    ciclo = np.append(caminho, caminho[0])  # Fechar o ciclo
    ax.plot(pontos[ciclo, 0], pontos[ciclo, 1], 'o-', markersize=10)

    ax.set_title("Gráfico dos pontos")
    ax.set_xlabel("coordenada x")
    ax.set_ylabel("coordenada y")
    ax.grid()

"""
# Função para visualizar o caminho gerado
def mostrar_caminho(pontos, caminho, ax):
    # Calcular o centro dos pontos
    centro = np.mean(pontos, axis=0)
    
    # Calcular ângulos dos pontos em relação ao centro
    angulos = np.arctan2(pontos[caminho, 1] - centro[1], pontos[caminho, 0] - centro[0])
    
    # Ordenar os índices dos pontos pelo ângulo
    ordem = np.argsort(angulos)
    
    # Obter o ciclo na ordem correta
    ciclo = np.append(np.array(caminho)[ordem], np.array(caminho)[ordem[0]])  # Fechar o ciclo

    # Plotar os pontos
    ax.plot(pontos[ciclo, 0], pontos[ciclo, 1], 'o-', markersize=10)

    ax.set_title("Gráfico dos pontos")
    ax.set_xlabel("coordenada x")
    ax.set_ylabel("coordenada y")
    ax.grid()
"""

# Função para gerar pontos aleatórios (uniforme ou em círculo)
def gerar_pontos_uniforme(n):
    return np.random.rand(n, 2) * 100

def gerar_pontos_circulo(n, raio=50):
    angulos = np.linspace(0, 2 * np.pi, n, endpoint=False)
    x = raio * np.cos(angulos) + raio
    y = raio * np.sin(angulos) + raio
    return np.column_stack((x, y))

# Função para medir o tempo de execução
def timx(func, *args):
    inicio = time.time()
    resultado = func(*args)
    fim = time.time()
    print(f"\nTempo de execução é: {fim - inicio:.2f} segundos\n\n")
    return resultado

# Parâmetros do algoritmo genético
tamanho_populacao = 100  # Escolhido para manter diversidade e bom desempenho
numero_geracoes = 500  # Permite exploração suficiente de soluções
taxa_mutacao = 0.09  # Mantém alguma variabilidade sem afetar muito a aptidão

# Preparação da figura para subplots
fig, axs = plt.subplots(3, 2, figsize=(14, 17))  # Aumentar a largura e altura

# Teste com 15 pontos (pontos uniformes)
pontos_uniformes = gerar_pontos_uniforme(15)
melhor_caminho, melhor_distancia, historico_15 = timx(algoritmo_genetico, pontos_uniformes, tamanho_populacao, numero_geracoes, taxa_mutacao)
mostrar_caminho(pontos_uniformes, melhor_caminho, axs[0, 0])

# Visualizar desempenho ao longo das gerações
axs[0, 1].plot(historico_15)
axs[0, 1].set_title("Desempenho ao longo das gerações - 15 pontos")
axs[0, 1].set_xlabel("Geração")
axs[0, 1].set_ylabel("Melhor distância")
axs[0, 1].grid()

# Teste com 100 pontos (distribuição circular)
pontos_mais = gerar_pontos_circulo(120)
melhor_caminho, melhor_distancia, historico_120 = timx(algoritmo_genetico, pontos_mais, tamanho_populacao, numero_geracoes, taxa_mutacao)
mostrar_caminho(pontos_mais, melhor_caminho, axs[1, 0])

axs[1, 1].plot(historico_120)
axs[1, 1].set_title("Desempenho ao longo das gerações - 120 pontos")
axs[1, 1].set_xlabel("Geração")
axs[1, 1].set_ylabel("Melhor distância")
axs[1, 1].grid()

# Teste com 200 pontos (circular) para o critério de alta quantidade de pontos
pontos_mais_x = gerar_pontos_circulo(280)
melhor_caminho, melhor_distancia, historico_280 = timx(algoritmo_genetico, pontos_mais_x, tamanho_populacao, numero_geracoes, taxa_mutacao)
mostrar_caminho(pontos_mais_x, melhor_caminho, axs[2, 0])

axs[2, 1].plot(historico_280)
axs[2, 1].set_title("Desempenho ao longo das gerações - 280 pontos")
axs[2, 1].set_xlabel("Geração")
axs[2, 1].set_ylabel("Melhor distância")
axs[2, 1].grid()

# Ajustar o layout para evitar sobreposição
plt.tight_layout()
plt.subplots_adjust(hspace=0.35, wspace=0.35)  # Ajustar espaçamentos entre subplots
plt.show()
