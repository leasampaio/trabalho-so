def round_robin(processos):

    tempo_atual = 0
    turnaround_total = 0
    resultados = []
    fila_processos = []
    qtd_processos=len(processos)

    dados_processos = {
        p.id: {
            "tempo_execucao": [],  # Lista de tuplas (inicio, fim) para cada período de execução
            "tempo_espera": [],  # Lista de tuplas (inicio, fim) para cada período de espera
            "turnaround": 0,
            "sobrecarga": [],  # Lista de tuplas (inicio, fim) para cada período de sobrecarga
            "tempo_chegada": 0,
            "turnaroundmedio":0
        }
        for p in processos
    }

    while processos or fila_processos:
        # Adiciona processos que chegaram ao tempo_atual à fila de processos
        processos_chegaram = [p for p in processos if p.tempo_chegada <= tempo_atual]
        for p in processos_chegaram:
            fila_processos.append(p)
            processos.remove(p)

        if not fila_processos:
            if processos:
                # Se não há processos prontos, avance o tempo para o próximo processo que chegará
                tempo_proximo = min(p.tempo_chegada for p in processos)
                tempo_atual = tempo_proximo
                continue
            else:
                break

        # Seleciona o próximo processo da fila de processos prontos
        processo_atual = fila_processos.pop(0)
        processo_atual.contador_execucao += 1

        # Executa o processo atual por até o quantum ou até terminar
        tempo_execucao = min(
            processo_atual.quantum_sistema, processo_atual.tempo_restante
        )
        inicio_execucao = tempo_atual
        fim_execucao = tempo_atual + tempo_execucao
        for p in fila_processos:
            if p.id != processo_atual.id:
                if tempo_atual > p.tempo_chegada and p.contador_execucao == 0:
                    gap_espera = 0
                    gap_espera = tempo_atual - p.tempo_chegada
                    inicio_espera = tempo_atual - gap_espera
                    dados_processos[p.id]["tempo_espera"].append(
                        {"inicio": inicio_espera, "fim": fim_execucao}
                    )
                else:
                    inicio_espera = tempo_atual
                    dados_processos[p.id]["tempo_espera"].append(
                        {"inicio": inicio_espera, "fim": fim_execucao}
                    )
        dados_processos[processo_atual.id]["tempo_execucao"].append(
            {"inicio": inicio_execucao, "fim": fim_execucao}
        )

        dados_processos[processo_atual.id][
            "quantum_sistema"
        ] = processo_atual.quantum_sistema

        processo_atual.tempo_restante -= tempo_execucao
        tempo_atual += tempo_execucao

        if "inicio" not in dados_processos[processo_atual.id]:
            dados_processos[processo_atual.id]["inicio"] = tempo_atual - tempo_execucao
            dados_processos[processo_atual.id]["fim"] = tempo_atual
            dados_processos[processo_atual.id]["id"] = processo_atual.id
            dados_processos[processo_atual.id][
                "tempo_chegada"
            ] = processo_atual.tempo_chegada

        if processo_atual.tempo_restante > 0:
            # Se o processo não terminou, coloque-o de volta no final da fila de prontos
            processos.append(processo_atual)
            sobrecarga_inicio = tempo_atual
            tempo_atual += processo_atual.sobrecarga_sistema
            sobrecarga_fim = tempo_atual

            dados_processos[processo_atual.id]["sobrecarga"].append(
                {"inicio": sobrecarga_inicio, "fim": sobrecarga_fim}
            )

            dados_processos[processo_atual.id]["fim"] = tempo_atual

        # Se o processo terminou, calcula os tempos de turnaround e espera
        if processo_atual.tempo_restante == 0:
            turnaround_processo = tempo_atual - processo_atual.tempo_chegada
            turnaround_total += turnaround_processo
            dados_processos[processo_atual.id]["turnaround"] = turnaround_processo
            tempo_espera = turnaround_processo - processo_atual.tempo_execucao
            dados_processos[processo_atual.id]["tempo_espera"].append(
                {
                    "inicio": dados_processos[processo_atual.id]["inicio"],
                    "fim": fim_execucao,
                }
            )

            # Atualiza o dicionário do processo com os dados finais

            dados_processos[processo_atual.id]["turnaroundmedio"] = turnaround_total/qtd_processos

            # Adiciona os dados do processo aos resultados

            resultados.append(dados_processos[processo_atual.id])

            print(
                f"Processo {processo_atual.id}: tempo_espera = {tempo_espera}, turnaround_processo = {turnaround_processo} chegada {processo_atual.tempo_chegada}"
            )

    # Adiciona a média do turnaround aos resultados
    media_turnaround = turnaround_total / len(processos) if processos else 0

    print("Resultados:", resultados)
    return resultados
