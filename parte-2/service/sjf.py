import copy


def sjf(processos):
    copia_processos = copy.deepcopy(processos)
    tempo_atual = 0
    resultados = []
    list_turnaround = []
    turnaround_total = 0

    while copia_processos:
        # Filtra processos que já chegaram e estão prontos para execução
        processos_prontos = [
            p for p in copia_processos if p.tempo_chegada <= tempo_atual
        ]
        if not processos_prontos:
            # Se nenhum processo está pronto, avança o tempo para o próximo processo que chegará
            tempo_proximo = min(p.tempo_chegada for p in copia_processos)
            tempo_atual = tempo_proximo
            continue

        # Seleciona o processo com o menor tempo de execução entre os prontos
        processo = min(processos_prontos, key=lambda p: p.tempo_execucao)

        # Remove o processo selecionado da lista
        copia_processos.remove(processo)

        # Calcula o tempo de espera e turnaround
        tempo_espera = tempo_atual - processo.tempo_chegada
        turnaround_processo = tempo_espera + processo.tempo_execucao
        turnaround_total += turnaround_processo
        list_turnaround.append(turnaround_processo)
        resultados.append(
            {
                "id": processo.id,
                "inicio": processo.tempo_chegada,
                "fim": processo.tempo_execucao,
                "tempo_espera": tempo_espera + processo.tempo_chegada,
                "turnaround": turnaround_processo,
                "Turnaround_Medio": turnaround_total / len(processos),
                "tempo_chegada": processo.tempo_chegada,
                "tempo_execucao": processo.tempo_execucao,
            }
        )

        # Imprime informações do processo
        print(
            f"Executando {processo} tempo_espera {tempo_espera} turnaround_processo = {turnaround_processo}"
        )

        # Atualiza o tempo atual após a execução do processo
        tempo_atual += processo.tempo_execucao
    # resultados.append(turnaround_total / qtdProcessos)
    print(resultados)
    return resultados
