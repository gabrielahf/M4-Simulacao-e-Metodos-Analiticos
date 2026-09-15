import heapq

# Gerador de numeros pseudoaleatorios
a = 16807
c = 0
M = 2147483647
seed = 123456789


class Fila:
    
    def __init__(self, servidores, capacidade,
                 atendimento_min, atendimento_max,
                 chegada_min=None, chegada_max=None):
        self.servidores = servidores
        self.capacidade = capacidade
        self.chegada_min = chegada_min      
        self.chegada_max = chegada_max
        self.atendimento_min = atendimento_min
        self.atendimento_max = atendimento_max

        self.clientes = 0
        self.servidores_ocupados = 0
        self.perdas = 0
        self.tempo_estado = [0.0] * (capacidade + 1)

    def tem_chegada_externa(self):
        return self.chegada_min is not None


def simular_rede(filas, roteamento, quantidade_aleatorios,
                  primeira_chegada, fila_entrada=0):
    

    ultimo = seed
    count = quantidade_aleatorios

    relogio = 0.0
    tempo_anterior = 0.0

    eventos = []
    sequencia = 0

    def next_random():
        nonlocal ultimo, count
        if count <= 0:
            return None
        ultimo = (a * ultimo + c) % M
        count -= 1
        return ultimo / M

    def agendar(tempo, tipo, fila_idx):
        nonlocal sequencia
        sequencia += 1
        heapq.heappush(eventos, (tempo, sequencia, tipo, fila_idx))

    def acumula_tempo(tempo):
        nonlocal tempo_anterior, relogio
        delta = tempo - tempo_anterior
        for fila in filas:
            fila.tempo_estado[fila.clientes] += delta
        tempo_anterior = tempo
        relogio = tempo

    def iniciar_atendimento(fila_idx):
        fila = filas[fila_idx]
        r = next_random()
        if r is None:
            return
        t = fila.atendimento_min + r * (fila.atendimento_max - fila.atendimento_min)
        agendar(relogio + t, "SAIDA", fila_idx)

    def rotear(fila_idx):
        opcoes = roteamento.get(fila_idx, [(None, 1.0)])
        if len(opcoes) == 1:
            return opcoes[0][0]

        r = next_random()
        if r is None:
            return None

        acumulado = 0.0
        for destino, probabilidade in opcoes:
            acumulado += probabilidade
            if r <= acumulado:
                return destino
        return opcoes[-1][0]

    def entra(fila_idx):
        fila = filas[fila_idx]
        if fila.clientes < fila.capacidade:
            fila.clientes += 1
            if fila.servidores_ocupados < fila.servidores:
                fila.servidores_ocupados += 1
                iniciar_atendimento(fila_idx)
        else:
            fila.perdas += 1

    # Agenda a primeira chegada externa na fila de entrada
    agendar(primeira_chegada, "CHEGADA", fila_entrada)

    while count > 0 and eventos:

        tempo, _, tipo, fila_idx = heapq.heappop(eventos)
        acumula_tempo(tempo)
        fila = filas[fila_idx]

        if tipo == "CHEGADA":
            entra(fila_idx)

            # Agenda a proxima chegada externa (somente para filas de entrada)
            if fila.tem_chegada_externa():
                r = next_random()
                if r is not None:
                    t = fila.chegada_min + r * (fila.chegada_max - fila.chegada_min)
                    agendar(relogio + t, "CHEGADA", fila_idx)

        elif tipo == "SAIDA":
            fila.clientes -= 1
            fila.servidores_ocupados -= 1

            # Existe cliente aguardando nesta fila?
            if fila.clientes > fila.servidores_ocupados and count > 0:
                fila.servidores_ocupados += 1
                iniciar_atendimento(fila_idx)

            # Roteia o cliente que saiu para a proxima fila (ou para fora da rede)
            destino = rotear(fila_idx)
            if destino is not None:
                agendar(relogio, "PASSAGEM", destino)

        elif tipo == "PASSAGEM":
            entra(fila_idx)

    return relogio, filas


def mostrar_resultado(nome, relogio, fila):

    print()
    print("=" * 55)
    print(nome)
    print("=" * 55)

    print(f"Numero de clientes perdidos: {fila.perdas}")
    print()

    print(
        f"{'Estado':<10}"
        f"{'Tempo acumulado':<20}"
        f"{'Probabilidade':<15}"
    )

    soma = 0.0

    for estado, tempo in enumerate(fila.tempo_estado):

        probabilidade = tempo / relogio if relogio > 0 else 0.0
        soma += probabilidade

        print(
            f"{estado:<10}"
            f"{tempo:<20.4f}"
            f"{probabilidade:<15.6f}"
        )

    print()
    print(
        f"{'Soma':<10}"
        f"{'':<20}"
        f"{soma:<15.6f}"
    )


if __name__ == "__main__":

    filas = [
        Fila(servidores=2, capacidade=3,
             chegada_min=1, chegada_max=5,
             atendimento_min=4, atendimento_max=5),
        Fila(servidores=1, capacidade=5,
             atendimento_min=1, atendimento_max=3),
    ]

    roteamento = {
        0: [(1, 1.0)],     
        1: [(None, 1.0)],  
    }

    relogio, filas_resultado = simular_rede(
        filas=filas,
        roteamento=roteamento,
        quantidade_aleatorios=100000,
        primeira_chegada=2.5,
        fila_entrada=0
    )

    print(f"\nTempo global da simulacao: {relogio:.4f}")

    mostrar_resultado("Fila 1 - G/G/2/3", relogio, filas_resultado[0])
    mostrar_resultado("Fila 2 - G/G/1/5", relogio, filas_resultado[1])