import copy


def edf(processos):
    copia_processos = copy.deepcopy(processos)
    tempo_atual = 0
    turnaround_total = 0
    resultados = []
    lista_aux = []

    dados_processos = {
        p.id: {
            "tempo_execucao": [],  # Lista de tuplas (inicio, fim) para cada período de execução
            "tempo_espera": [],  # Lista de tuplas (inicio, fim) para cada período de espera
            "turnaround": 0,
            "sobrecarga": [],  # Lista de tuplas (inicio, fim) para cada período de sobrecarga
            "tempo_chegada": p.tempo_chegada,
            "inicio": None,
            "fim": None,
            "deadline": p.deadline,
            "estouro_deadline": False,
        }
        for p in processos
    }

    while copia_processos:
        # Filtra processos que já chegaram e estão prontos para execução
        processos_prontos = [
            p for p in copia_processos if p.tempo_chegada <= tempo_atual
        ]

        if not processos_prontos:
            # Se nenhum processo está pronto, avança o tempo para o próximo processo que chegará
            if copia_processos:
                tempo_proximo = min(p.tempo_chegada for p in copia_processos)
                tempo_atual = tempo_proximo
                continue
            else:
                break

        # Seleciona o processo com o menor tempo de deadline entre os prontos
        processo = min(processos_prontos, key=lambda p: p.deadline)

        if processo.tempo_restante == 0:
            processo.tempo_restante = processo.tempo_execucao

        inicio_execucao = tempo_atual
        tempo_execucao = min(processo.quantum_sistema, processo.tempo_restante)
        fim_execucao = tempo_atual + tempo_execucao

        for p in processos_prontos:
            if p.id != processo.id:
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

        # Decrementa do tempo restante
        while processo.tempo_restante > 0:
            processo.contador_execucao += 1
            processo.tempo_restante -= tempo_execucao
            tempo_atual += tempo_execucao

            dados_processos[processo.id]["tempo_execucao"].append(
                {"inicio": inicio_execucao, "fim": fim_execucao}
            )
            processos_prontos = [
                p for p in copia_processos if p.tempo_chegada <= tempo_atual
            ]

            if processos_prontos:
                processo_aux = min(processos_prontos, key=lambda p: p.deadline)
                if (
                    tempo_atual >= processo_aux.tempo_chegada
                    and processo.deadline > processo_aux.deadline
                ):
                    if processo.tempo_chegada != 0:
                        tempo_espera = tempo_atual - processo.tempo_execucao
                    lista_aux.append(processo)
                    tempo_espera_inicio = tempo_atual
                    copia_processos.remove(processo)
                    tempo_atual += processo.sobrecarga_sistema

                    for p in processos_prontos:
                        if p.id != processo.id:
                            if (
                                tempo_atual > p.tempo_chegada
                                and p.contador_execucao == 0
                            ):
                                gap_espera = 0
                                gap_espera = tempo_atual - p.tempo_chegada
                                inicio_espera = tempo_atual - gap_espera
                                dados_processos[p.id]["tempo_espera"].append(
                                    {"inicio": tempo_espera_inicio, "fim": tempo_atual}
                                )
                            else:
                                inicio_espera = tempo_atual
                                dados_processos[p.id]["tempo_espera"].append(
                                    {"inicio": inicio_espera, "fim": fim_execucao}
                                )
                    dados_processos[processo.id]["sobrecarga"].append(
                        {
                            "inicio": tempo_atual - processo.sobrecarga_sistema,
                            "fim": tempo_atual,
                        }
                    )

                    break

            # Checa se o processo atingiu o quantum
            if processo_aux.tempo_restante != 0:
                tempo_espera_inicio = tempo_atual
                tempo_atual += processo.sobrecarga_sistema
                processo.contador_quantum = 0

                dados_processos[processo.id]["sobrecarga"].append(
                    {
                        "inicio": tempo_atual - processo.sobrecarga_sistema,
                        "fim": tempo_atual,
                    }
                )
                for p in processos_prontos:
                    if p.id != processo.id:
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
                                {"inicio": tempo_espera_inicio, "fim": tempo_atual}
                            )
                dados_processos[processo.id]["tempo_execucao"].append(
                    {"inicio": inicio_execucao, "fim": fim_execucao}
                )

                break

        # Remove o processo selecionado da lista
        if processo.tempo_restante == 0:
            processos_prontos.remove(processo)
            copia_processos.remove(processo)

            turnaround_processo = tempo_atual - processo.tempo_chegada
            tempo_espera = turnaround_processo - processo.tempo_execucao
            turnaround_total += turnaround_processo

            dados_processos[processo.id]["turnaround"] = turnaround_processo
            dados_processos[processo.id]["tempo_execucao"].append(
                {"inicio": inicio_execucao, "fim": tempo_atual}
            )
            dados_processos[processo.id]["inicio"] = inicio_execucao
            dados_processos[processo.id]["fim"] = tempo_atual
            dados_processos[processo.id]["id"] = processo.id
            if turnaround_processo > processo.deadline:
                dados_processos[processo.id]["estouro_deadline"] = True

            resultados.append(dados_processos[processo.id])

            print(
                f"Executando {processo} tempo_espera {tempo_espera} turnaround_processo = {turnaround_processo}"
            )

        # Adiciona processos pausados de volta à lista de processos
        copia_processos.extend(lista_aux)
        lista_aux.clear()

    # Calcula a média de turnaround e adiciona ao resultado final

    media_turnaround = turnaround_total / len(processos) if processos else 0
    print(media_turnaround)
    # Mostra os dados dos processos
    print(resultados)

    return resultados
