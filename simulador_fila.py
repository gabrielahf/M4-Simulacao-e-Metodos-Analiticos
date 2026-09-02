import heapq


# Gerador de numeros pseudoaleatorios
a = 16807
c = 0
M = 2147483647
seed = 123456789


def simular(servidores, capacidade,
            chegada_min, chegada_max,
            atendimento_min, atendimento_max,
            quantidade_aleatorios,
            primeira_chegada):

    ultimo = seed
    count = quantidade_aleatorios

    relogio = 0.0
    tempo_anterior = 0.0

    estado = 0
    servidores_ocupados = 0
    perdas = 0

    tempo_estado = [0.0] * (capacidade + 1)

    eventos = []
    sequencia = 0

    def NextRandom():
        nonlocal ultimo, count

        if count <= 0:
            return None

        ultimo = (a * ultimo + c) % M
        count -= 1

        return ultimo / M

    def agendar(tempo, tipo):
        nonlocal sequencia

        sequencia += 1
        heapq.heappush(eventos, (tempo, sequencia, tipo))

    # Primeira chegada
    agendar(primeira_chegada, "CHEGADA")

    while count > 0 and eventos:

        tempo, _, tipo = heapq.heappop(eventos)

        delta = tempo - tempo_anterior
        tempo_estado[estado] += delta

        tempo_anterior = tempo
        relogio = tempo

        if tipo == "CHEGADA":

            if estado < capacidade:

                estado += 1

                if servidores_ocupados < servidores:

                    servidores_ocupados += 1

                    r = NextRandom()

                    if r is not None:
                        t = atendimento_min + r * (
                            atendimento_max - atendimento_min
                        )

                        agendar(
                            relogio + t,
                            "SAIDA"
                        )

            else:
                perdas += 1

            # Agenda a proxima chegada
            r = NextRandom()

            if r is not None:
                t = chegada_min + r * (
                    chegada_max - chegada_min
                )

                agendar(
                    relogio + t,
                    "CHEGADA"
                )

        else:

            estado -= 1
            servidores_ocupados -= 1

            # Verifica se existe cliente aguardando
            if estado > servidores_ocupados and count > 0:

                servidores_ocupados += 1

                r = NextRandom()

                if r is not None:
                    t = atendimento_min + r * (
                        atendimento_max - atendimento_min
                    )

                    agendar(
                        relogio + t,
                        "SAIDA"
                    )

    return relogio, perdas, tempo_estado


def mostrar_resultado(nome, relogio, perdas, tempo_estado):

    print()
    print("=" * 55)
    print(nome)
    print("=" * 55)

    print(f"Tempo global da simulacao: {relogio:.4f}")
    print(f"Numero de clientes perdidos: {perdas}")
    print()

    print(
        f"{'Estado':<10}"
        f"{'Tempo acumulado':<20}"
        f"{'Probabilidade':<15}"
    )

    soma = 0.0

    for estado, tempo in enumerate(tempo_estado):

        probabilidade = (
            tempo / relogio
            if relogio > 0
            else 0.0
        )

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


# G/G/1/5

tempo, perdas, estados = simular(
    servidores=1,
    capacidade=5,
    chegada_min=3,
    chegada_max=5,
    atendimento_min=4,
    atendimento_max=5,
    quantidade_aleatorios=100000,
    primeira_chegada=3.0
)

mostrar_resultado(
    "Fila G/G/1/5",
    tempo,
    perdas,
    estados
)


# G/G/2/5

tempo, perdas, estados = simular(
    servidores=2,
    capacidade=5,
    chegada_min=3,
    chegada_max=5,
    atendimento_min=4,
    atendimento_max=5,
    quantidade_aleatorios=100000,
    primeira_chegada=3.0
)

mostrar_resultado(
    "Fila G/G/2/5",
    tempo,
    perdas,
    estados
)