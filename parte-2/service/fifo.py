def fifo(processos):
    tempo_atual = 0
    resultados = []
    turnaround_total = 0
    # Ordena os processos pelo tempo de chegada
    processos_ordenados = sorted(processos, key=lambda p: p.tempo_chegada)

    for processo in processos_ordenados:
        # Atualiza o tempo atual se for menor que o tempo de chegada do process
        if tempo_atual < processo.tempo_chegada:
            tempo_atual = processo.tempo_chegada

        # Calcula o tempo de espera e o turnaround do processo

        tempo_espera = tempo_atual - processo.tempo_chegada
        turnaround_processo = tempo_espera + processo.tempo_execucao
        turnaround_total += turnaround_processo

        # Adiciona os resultados à lista
        resultados.append(
            {
                "id": processo.id,
                "inicio": processo.tempo_chegada,
                "fim": processo.tempo_execucao,
                "tempo_espera": tempo_espera + processo.tempo_chegada,
                "turnaround": turnaround_processo,
                "turnaroundmedio": turnaround_total / len(processos),
                "tempo_chegada": processo.tempo_chegada,
                "tempo_execucao": processo.tempo_execucao,
            }
        )

        

        # Atualiza o tempo atual após a execução do processo
        tempo_atual += processo.tempo_execucao
    # resultados.append(turnaround_total / len(processos))
     
    return resultados
