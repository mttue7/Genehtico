# Algoritmo Genético para o Problema do Caixeiro Viajante (TSP)

Este projeto implementa um algoritmo genético para resolver uma versão adaptada do problema do Caixeiro Viajante (TSP - Traveling Salesman Problem), onde o objetivo é encontrar o caminho mais curto que passa por uma série de pontos distribuídos em duas dimensões. Além de resolver o problema, a implementação permite a visualização e comparação de resultados com diferentes conjuntos de pontos.

## Objetivo
O problema do Caixeiro Viajante é um clássico em otimização combinatória e é NP-difícil, ou seja, demanda muito processamento para encontrar soluções ótimas em grandes instâncias. Este projeto visa demonstrar o uso de algoritmos genéticos como uma abordagem heurística para encontrar soluções satisfatórias de forma mais rápida e eficiente.

## Principais Funcionalidades
- **Geração de pontos de teste**: Suporta a criação de conjuntos de pontos distribuídos de forma aleatória ou circular.
- **Implementação do Algoritmo Genético**: Utiliza seleção por torneio, cruzamento por ordem (OX), mutação e um critério de parada para otimização do percurso.
- **Visualização dos Resultados**: Exibe o percurso calculado para diferentes tamanhos de conjuntos de pontos, além de gráficos de desempenho ao longo das gerações.

## Estrutura do Código
- **Funções de Otimização**:
  - `calcular_distancia`: Calcula a distância euclidiana entre dois pontos.
  - `aptidao`: Avalia a "aptidão" de um caminho, baseada na distância total percorrida.
  - `gerar_populacao`: Gera uma população inicial aleatória de caminhos.
  - `crossover`: Implementa o operador de cruzamento por ordem (OX) para criar filhos.
  - `mutacao`: Realiza a mutação por inversão de posições para manter a variabilidade.
  - `selecao`: Seleção por torneio para escolher os melhores indivíduos.
- **Funções de Visualização**:
  - `mostrar_caminho`: Exibe o caminho gerado em um gráfico.
  - Gráficos de desempenho ao longo das gerações.
  
## Parâmetros de Configuração
- **`tamanho_populacao`**: Número de indivíduos na população, ajustado para garantir diversidade.
- **`numero_geracoes`**: Quantidade máxima de gerações, permitindo exploração suficiente de soluções.
- **`taxa_mutacao`**: Taxa de mutação para manter variabilidade sem perder aptidão.

## Exemplos de Uso

Para visualizar e comparar o desempenho do algoritmo com diferentes tamanhos de conjuntos de pontos (15, 120 e 280 pontos), o código gera gráficos comparativos. 

Para executar o projeto, rode o arquivo `.py` em um ambiente Python com as bibliotecas necessárias:

```bash
python gen.py
```

## Visualização dos Resultados
Cada execução gera subplots para os caminhos e para o desempenho ao longo das gerações, conforme abaixo:

- **Gráficos de Caminho**: Exibem o percurso gerado para conjuntos de 10, 100 e 200 pontos, com distribuição aleatória e circular.
- **Gráficos de Desempenho**: Visualizam a melhor distância encontrada ao longo das gerações para cada conjunto de pontos.

## Dependências
Para executar este projeto, você precisará das seguintes bibliotecas:

- ```numpy```
- ```matplotlib```

Instale as dependências com o seguinte comando:
bash
```
pip install numpy matplotlib
```

## Observação
Este projeto é uma implementação acadêmica, desenvolvida para demonstrar o uso de algoritmos genéticos em problemas de otimização. Ajustes podem ser feitos para aprimorar o desempenho em casos específicos.