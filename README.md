# Simulação e Métodos Analíticos

Este repositório reúne dois simuladores desenvolvidos para estudar comportamento de filas e redes de filas em contexto de modelagem e simulação analítica.

A estrutura está organizada em duas partes principais:

- M4: `simulador_fila.py` — simulação de uma fila clássica com múltiplos servidores e capacidade finita
- M6: `simulador_tandem.py` — simulação de uma rede em tandem com roteamento entre filas

---

## Objetivo geral

Os scripts foram criados para explorar conceitos de:

- geração de números pseudoaleatórios;
- eventos discretos;
- filas com capacidade limitada;
- servidores múltiplos;
- perdas por saturação;
- estado da fila ao longo do tempo;
- redes de filas em tandem.

A ideia é reproduzir cenários reais de atendimento e analisar estatísticas como:

- tempo total de simulação;
- número de clientes perdidos;
- distribuição do estado da fila ao longo do tempo;
- probabilidade de ocupação de cada nível de fila.

---

## M4 — Simulador de fila

Arquivo: `simulador_fila.py`

### O que simula

Este módulo representa uma fila do tipo G/G/s/K, isto é:

- chegadas com distribuição geral (G);
- atendimentos com distribuição geral (G);
- s servidores;
- capacidade total K para clientes no sistema.

No exemplo principal, a simulação considera:

- `G/G/1/5` → 1 servidor e capacidade 5
- `G/G/2/5` → 2 servidores e capacidade 5

### Componentes principais

- gerador de números pseudoaleatórios com congruência linear;
- fila de eventos organizada por heap (`heapq`);
- calendário de eventos com chegadas e saídas;
- contabilização do tempo em cada estado da fila;
- medição das perdas por overflow.

### Estrutura da lógica

A função `simular(...)` recebe parâmetros como:

- `servidores`: quantidade de servidores
- `capacidade`: limite da fila/sistema
- `chegada_min`, `chegada_max`: intervalo de chegada
- `atendimento_min`, `atendimento_max`: tempo de atendimento
- `quantidade_aleatorios`: quantidade de gerados para a simulação
- `primeira_chegada`: instante da primeira chegada

A simulação funciona da seguinte forma:

1. Agenda a primeira chegada;
2. Processa eventos em ordem cronológica;
3. Atualiza o tempo acumulado em cada estado;
4. Se a fila está vazia e há servidores livres, inicia atendimento;
5. Se a fila está cheia, contabiliza perda;
6. Reagenda novas chegadas e saídas conforme o processo.

### Saída esperada

Ao executar o script, ele imprime:

- tempo global da simulação;
- número de clientes perdidos;
- tabela com estado da fila e tempo acumulado;
- probabilidade de cada estado;
- soma das probabilidades.

### Exemplo de execução

```bash
python simulador_fila.py
```

---

## M6 — Simulador em tandem

Arquivo: `simulador_tandem.py`

### O que simula

Este módulo modela uma rede de filas em tandem, ou seja, múltiplas filas em sequência, onde clientes saem de uma fila e passam para a próxima.

Ele utiliza a classe `Fila` para encapsular cada etapa do sistema e a função `simular_rede(...)` para processar a rede inteira.

### Estrutura da rede

No exemplo configurado, há duas filas:

- Fila 1: `G/G/2/3`
  - 2 servidores
  - capacidade 3
  - chegada externa
- Fila 2: `G/G/1/5`
  - 1 servidor
  - capacidade 5
  - sem chegada externa, recebe clientes da fila anterior

A rede define o roteamento:

- clientes saem da fila 1 e seguem para a fila 2;
- após a fila 2, saem da rede.

### Componentes principais

- `Fila`: estrutura que guarda:
  - quantidade de servidores;
  - capacidade;
  - intervalos de chegada e atendimento;
  - clientes presentes;
  - servidores ocupados;
  - perdas;
  - tempo acumulado por estado.
- `simular_rede(...)`: executa a simulação em eventos discretos para todas as filas;
- `rotear(...)`: define para onde cada cliente segue após a saída;
- `agendar(...)`: registra eventos no calendário de eventos.

### Fluxo da simulação

1. Agenda a primeira chegada externa na fila de entrada;
2. Processa eventos de chegada, saída e passagem;
3. Quando um cliente sai de uma fila, ele é roteado para a próxima fila ou para fora do sistema;
4. A fila atualiza número de clientes, ocupação dos servidores e estado;
5. Se houver clientes esperando, novos atendimentos são iniciados;
6. O processo continua até o fim do número de aleatórios gerados ou sem eventos pendentes.

### Observações importantes

- As filas podem ter ou não chegada externa.
- `PASSAGEM` é um evento interno da rede.
- O tempo global da simulação é compartilhado por todas as filas.
- Cada fila mantém seu próprio histórico de ocupação e perdas.

### Saída esperada

O script imprime:

- tempo global da simulação;
- perdas por fila;
- tabela de estado da fila;
- probabilidade de ocupação de cada nível;
- soma das probabilidades.

### Exemplo de execução

```bash
python simulador_tandem.py
```

---

## Comparação entre os módulos

| Módulo | Tipo | Característica principal |
|---|---|---|
| `simulador_fila.py` | Fila simples | Modela uma fila isolada com múltiplos servidores e capacidade finita |
| `simulador_tandem.py` | Rede de filas | Modela múltiplas filas conectadas e roteamento entre elas |

A diferença principal é que o M4 trata uma única fila em operação, enquanto o M6 expande o problema para uma topologia de atendimento em série, mais próxima de sistemas reais de produção, serviços e redes de filas.

---

## Tecnologias e bibliotecas

O projeto usa apenas módulos da biblioteca padrão do Python:

- `heapq` para gerenciamento da fila de eventos;
- estruturas nativas de Python para listas, dicionários e controle do fluxo.

Não há dependências externas, o que facilita execução em qualquer ambiente com Python instalado.

---

## Requisitos

- Python 3.x
- Ambiente terminal/CLI

---

## Conclusão

Este repositório oferece uma visão prática de simulação de filas e redes em tandem, com foco em:

- eventos discretos;
- análise probabilística de ocupação;
- capacidade finita;
- perdas de clientes;
- sistemas de atendimento com múltiplos estágios.

Esses modelos servem como base para estudos de teoria das filas, processos estocásticos e aplicações em logística, serviços, telecomunicações e operação de sistemas.
