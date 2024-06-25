class Processo:
    def __init__(self, id, tempo_chegada, tempo_execucao, deadline, quantum_sistema, sobrecarga_sistema):
        self.id = id
        self.tempo_chegada = tempo_chegada
        self.tempo_execucao = tempo_execucao
        self.deadline = deadline
        self.quantum_sistema = quantum_sistema
        self.sobrecarga_sistema = sobrecarga_sistema
        self.tempo_restante = tempo_execucao

    def __repr__(self):
        return (f"Processo(id={self.id}, tempo_chegada={self.tempo_chegada}, "
                f"tempo_execucao={self.tempo_execucao}, deadline={self.deadline}, "
                f"tempo_restante={self.tempo_restante})")


def fifo(processos):
    tempo_atual = 0
    for processo in processos:
        if tempo_atual < processo.tempo_chegada:
            tempo_atual = processo.tempo_chegada
        print(f"Executando {processo} no tempo {tempo_atual}")
        tempo_atual += processo.tempo_execucao + processo.sobrecarga_sistema


def sjf(processos):
    processos_ordenados = sorted(processos, key=lambda p: (p.tempo_chegada, p.tempo_execucao))
    fifo(processos_ordenados)


def round_robin(processos, quantum):
    fila = processos[:]
    tempo_atual = 0

    while fila:
        processo = fila.pop(0)
        if tempo_atual < processo.tempo_chegada:
            tempo_atual = processo.tempo_chegada
        
        tempo_executado = min(processo.tempo_restante, quantum)
        processo.tempo_restante -= tempo_executado
        print(f"Executando {processo} no tempo {tempo_atual}")
        tempo_atual += tempo_executado + processo.sobrecarga_sistema

        if processo.tempo_restante > 0:
            fila.append(processo)


def edf(processos):
    processos_ordenados = sorted(processos, key=lambda p: (p.deadline, p.tempo_chegada))
    fifo(processos_ordenados)


# Exemplo de uso
def main():
    quantum_sistema = 4
    sobrecarga_sistema = 1

    lista_processos = [
        Processo(1, 0, 8, 10, quantum_sistema, sobrecarga_sistema),
        Processo(2, 1, 4, 12, quantum_sistema, sobrecarga_sistema),
        Processo(3, 2, 9, 14, quantum_sistema, sobrecarga_sistema),
        Processo(4, 3, 5, 16, quantum_sistema, sobrecarga_sistema),
    ]

    print("FIFO:")
    fifo(lista_processos[:])

    print("\nSJF:")
    sjf(lista_processos[:])

    print("\nRound Robin:")
    round_robin(lista_processos[:], quantum_sistema)

    print("\nEDF:")
    edf(lista_processos[:])


if __name__ == "__main__":
    main()
