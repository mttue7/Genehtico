import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import random
import matplotlib.pyplot as plt
import time

# Classe Gene para representar uma cidade
class Gene:
    def __init__(self, cidade_id):
        self.cidade_id = cidade_id

# Classe Individuo para representar um caminho
class Individuo:
    def __init__(self, genes):
        self.genes = genes
        self.aptidao = None

# Função para calcular a distância euclidiana entre dois pontos
def calcular_distancia(ponto1, ponto2):
    return np.sqrt(np.sum((ponto1 - ponto2) ** 2))

# Função de aptidão: calcula a soma total da distância percorrida no ciclo
def aptidao(individuo, pontos):
    caminho = [gene.cidade_id for gene in individuo.genes]
    distancia_total = 0
    for i in range(len(caminho)):
        distancia_total += calcular_distancia(pontos[caminho[i]], pontos[caminho[(i + 1) % len(caminho)]])
    individuo.aptidao = distancia_total
    return distancia_total

# Geração inicial de população aleatória
def gerar_populacao(pontos, tamanho_populacao):
    populacao = []
    for _ in range(tamanho_populacao):
        genes = [Gene(cidade_id) for cidade_id in np.random.permutation(len(pontos))]
        populacao.append(Individuo(genes))
    return populacao

# Operador de cruzamento (crossover por ordem - OX)
def crossover(pai1, pai2):
    corte1, corte2 = sorted(random.sample(range(len(pai1.genes)), 2))
    filho_genes = [None] * len(pai1.genes)
    
    # Copia parte do pai1
    filho_genes[corte1:corte2] = pai1.genes[corte1:corte2]
    posicao = corte2
    
    # Completa com os genes do pai2
    for gene in pai2.genes:
        if gene not in filho_genes:
            if posicao >= len(pai1.genes):
                posicao = 0
            filho_genes[posicao] = gene
            posicao += 1

    return Individuo(filho_genes)

# Operador de mutação (inversão de duas posições aleatórias)
def mutacao(individuo, taxa_mutacao):
    if random.random() < taxa_mutacao:
        i, j = sorted(random.sample(range(len(individuo.genes)), 2))
        individuo.genes[i:j] = individuo.genes[i:j][::-1]
    return individuo

# Seleção por torneio
def selecao(populacao, pontos, k=3):
    torneio = random.sample(populacao, k)
    torneio.sort(key=lambda individuo: aptidao(individuo, pontos))
    return torneio[0]

# Função principal do algoritmo genético
def algoritmo_genetico(pontos, tamanho_populacao, numero_geracoes, taxa_mutacao):
    populacao = gerar_populacao(pontos, tamanho_populacao)
    melhor_caminho = None
    melhor_distancia = float('inf')
    historico_aptidao = []

    repeticoes_consecutivas = 0
    ultima_aptidao = None

    for geracao in range(numero_geracoes):
        nova_populacao = []
        for _ in range(tamanho_populacao // 2):
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

        if melhor_aptidao == ultima_aptidao:
            repeticoes_consecutivas += 1
        else:
            repeticoes_consecutivas = 0

        ultima_aptidao = melhor_aptidao

        if repeticoes_consecutivas >= 80:
            print("Critério de parada atingido: Melhor aptidão repetida por 80 gerações")
            break

        if melhor_aptidao < melhor_distancia:
            melhor_distancia = melhor_aptidao
            melhor_caminho = melhor_individuo

        historico_aptidao.append(melhor_distancia)
        print(f"Geração {geracao}: Melhor distância = {melhor_distancia:.3f}")

    return melhor_caminho, melhor_distancia, historico_aptidao


# Função para visualizar o caminho gerado
def mostrar_caminho(pontos, caminho, ax):
    ordem_cidades = [gene.cidade_id for gene in caminho.genes]
    ciclo = np.append(ordem_cidades, ordem_cidades[0])

    ax.plot(pontos[ciclo, 0], pontos[ciclo, 1], 'o-', markersize=10)
    ax.set_title("Gráfico dos pontos")
    ax.set_xlabel("coordenada x")
    ax.set_ylabel("coordenada y")
    ax.grid()

# Função para gerar pontos aleatórios (uniforme ou em círculo)
def gerar_pontos_uniforme(n):
    return np.random.rand(n, 2) * 100

#função que confere o centro do circulo e atraves de calculos em relação ao raio, me entrega um "circulo"
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

# Parâmetros utilizados
tamanho_populacao = 100
numero_geracoes = 500  
taxa_mutacao = 0.09 

"""
Definimos o tamanho da população como 100 para garantir uma boa diversidade de soluções. 
Já o número de gerações (500) foi escolhido para dar tempo suficiente 
ao algoritmo para explorar e melhorar as soluções encontradas. 
A taxa de mutação (0.09) foi ajustada para manter certa variabilidade, 
evitando que o algoritmo fique preso em soluções ruins 
sem, ao mesmo tempo, gerar tanta aleatoriedade a ponto de desfazer o progresso feito.
"""

fig, axs = plt.subplots(6, 2, figsize=(19, 35))
plt.subplots_adjust(hspace=0.4, wspace=0.4)

# Teste com 15 pontos (pontos uniformes)
pontos_uniformes = gerar_pontos_uniforme(15)
melhor_caminho, melhor_distancia, historico_15 = timx(algoritmo_genetico, pontos_uniformes, tamanho_populacao, numero_geracoes, taxa_mutacao)
mostrar_caminho(pontos_uniformes, melhor_caminho, axs[0, 0])

# Função de interface gráfica com rolagem
def exibir_interface():
    root = tk.Tk()
    root.title("Visualização dos Gráficos")
    root.geometry("1500x1500")

    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=1)
    canvas = tk.Canvas(main_frame)
    scrollbar = tk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def on_mouse_wheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    canvas.bind_all("<MouseWheel>", on_mouse_wheel)

    # Preparação da figura para subplots
    fig, axs = plt.subplots(6, 2, figsize=(19, 35))
    plt.subplots_adjust(hspace=0.4, wspace=0.4)

    # 15 pontos
    pontos_uniformes_15 = gerar_pontos_uniforme(15)
    melhor_caminho, melhor_distancia, historico_15 = timx(algoritmo_genetico, pontos_uniformes_15, tamanho_populacao, numero_geracoes, taxa_mutacao)
    mostrar_caminho(pontos_uniformes_15, melhor_caminho, axs[0, 0])
    axs[0, 1].plot(historico_15)
    axs[0, 1].set_title("Desempenho ao longo das gerações - 15 pontos (Uniforme)")
    axs[0, 1].grid()

    pontos_circulo_15 = gerar_pontos_circulo(15)
    melhor_caminho, melhor_distancia, historico_15_circ = timx(algoritmo_genetico, pontos_circulo_15, tamanho_populacao, numero_geracoes, taxa_mutacao)
    mostrar_caminho(pontos_circulo_15, melhor_caminho, axs[1, 0])
    axs[1, 1].plot(historico_15_circ)
    axs[1, 1].set_title("Desempenho ao longo das gerações - 15 pontos (Circular)")
    axs[1, 1].grid()

    # 120 pontos
    pontos_uniformes_120 = gerar_pontos_uniforme(120)
    melhor_caminho, melhor_distancia, historico_120 = timx(algoritmo_genetico, pontos_uniformes_120, tamanho_populacao, numero_geracoes, taxa_mutacao)
    mostrar_caminho(pontos_uniformes_120, melhor_caminho, axs[2, 0])
    axs[2, 1].plot(historico_120)
    axs[2, 1].set_title("Desempenho ao longo das gerações - 120 pontos (Uniforme)")
    axs[2, 1].grid()

    pontos_circulo_120 = gerar_pontos_circulo(120)
    melhor_caminho, melhor_distancia, historico_120_circ = timx(algoritmo_genetico, pontos_circulo_120, tamanho_populacao, numero_geracoes, taxa_mutacao)
    mostrar_caminho(pontos_circulo_120, melhor_caminho, axs[3, 0])
    axs[3, 1].plot(historico_120_circ)
    axs[3, 1].set_title("Desempenho ao longo das gerações - 120 pontos (Circular)")
    axs[3, 1].grid()

    # 280 pontos
    pontos_uniformes_280 = gerar_pontos_uniforme(280)
    melhor_caminho, melhor_distancia, historico_280 = timx(algoritmo_genetico, pontos_uniformes_280, tamanho_populacao, numero_geracoes, taxa_mutacao)
    mostrar_caminho(pontos_uniformes_280, melhor_caminho, axs[4, 0])
    axs[4, 1].plot(historico_280)
    axs[4, 1].set_title("Desempenho ao longo das gerações - 280 pontos (Uniforme)")
    axs[4, 1].grid()

    pontos_circulo_280 = gerar_pontos_circulo(280)
    melhor_caminho, melhor_distancia, historico_280_circ = timx(algoritmo_genetico, pontos_circulo_280, tamanho_populacao, numero_geracoes, taxa_mutacao)
    mostrar_caminho(pontos_circulo_280, melhor_caminho, axs[5, 0])
    axs[5, 1].plot(historico_280_circ)
    axs[5, 1].set_title("Desempenho ao longo das gerações - 280 pontos (Circular)")
    axs[5, 1].grid()

    plt.tight_layout()

    canvas_fig = FigureCanvasTkAgg(fig, scrollable_frame)
    canvas_fig.get_tk_widget().pack()

    root.mainloop()

exibir_interface()