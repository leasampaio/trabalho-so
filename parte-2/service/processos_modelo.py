class Processo:
    def __init__(
        self,
        id,
        tempo_chegada,
        tempo_execucao,
        deadline,
        quantum_sistema,
        sobrecarga_sistema,
    ):
        self.id = id
        self.tempo_chegada = tempo_chegada
        self.tempo_execucao = tempo_execucao
        self.deadline = deadline
        self.quantum_sistema = quantum_sistema
        self.sobrecarga_sistema = sobrecarga_sistema
        self.tempo_restante = tempo_execucao
        self.contador_quantum = 0
        self.contador_execucao = 0

    def __repr__(self):
        return (
            f"Processo(id={self.id}, tempo_chegada={self.tempo_chegada}, "
            f"tempo_execucao={self.tempo_execucao}, deadline={self.deadline}, "
            f"tempo_restante={self.tempo_restante}"
        )

