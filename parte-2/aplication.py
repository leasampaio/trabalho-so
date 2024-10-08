# import copy
# from bokeh.io import output_file, save

# import matplotlib.pyplot as plt
# from bokeh.models import ColumnDataSource, FactorRange
# from bokeh.plotting import figure, show
# from bokeh.io import curdoc

# from bokeh.models import ColumnDataSource, FactorRange, SingleIntervalTicker


# import pandas as pd


# class Processo:
#     def __init__(
#         self,
#         id,
#         tempo_chegada,
#         tempo_execucao,
#         deadline,
#         quantum_sistema,
#         sobrecarga_sistema,
#     ):
#         self.id = id
#         self.tempo_chegada = tempo_chegada
#         self.tempo_execucao = tempo_execucao
#         self.deadline = deadline
#         self.quantum_sistema = quantum_sistema
#         self.sobrecarga_sistema = sobrecarga_sistema
#         self.tempo_restante = tempo_execucao
#         self.contador_quantum = 0
#         self.contador_execucao = 0

#     def __repr__(self):
#         return (
#             f"Processo(id={self.id}, tempo_chegada={self.tempo_chegada}, "
#             f"tempo_execucao={self.tempo_execucao}, deadline={self.deadline}, "
#             f"tempo_restante={self.tempo_restante}"
#         )


# def fifo(processos: Processo):
#     tempo_atual = 0
#     resultados = []
#     turnaround_total = 0
#     # Ordena os processos pelo tempo de chegada
#     processos_ordenados = sorted(processos, key=lambda p: p.tempo_chegada)

#     for processo in processos_ordenados:
#         # Atualiza o tempo atual se for menor que o tempo de chegada do process
#         if tempo_atual < processo.tempo_chegada:
#             tempo_atual = processo.tempo_chegada

#         # Calcula o tempo de espera e o turnaround do processo

#         tempo_espera = tempo_atual - processo.tempo_chegada
#         turnaround_processo = tempo_espera + processo.tempo_execucao
#         turnaround_total += turnaround_processo

#         # Adiciona os resultados à lista
#         resultados.append(
#             {
#                 "id": processo.id,
#                 "inicio": processo.tempo_chegada,
#                 "fim": processo.tempo_execucao,
#                 "tempo_espera": tempo_espera + processo.tempo_chegada,
#                 "turnaround": turnaround_processo,
#                 "Turnaround_Medio": turnaround_total / len(processos),
#                 "tempo_chegada": processo.tempo_chegada,
#                 "tempo_execucao": processo.tempo_execucao,
#             }
#         )

#         print(
#             f"Executando {processo} tempo_espera {tempo_espera} turnaround_processo = {turnaround_processo}"
#         )

#         # Atualiza o tempo atual após a execução do processo
#         tempo_atual += processo.tempo_execucao
#     # resultados.append(turnaround_total / len(processos))
#     print(f"turnaround_total = {turnaround_total}")

#     print(resultados)
#     return resultados


# def sjf(processos):
#     copia_processos = copy.deepcopy(processos)
#     tempo_atual = 0
#     resultados = []
#     list_turnaround = []
#     turnaround_total = 0

#     while copia_processos:
#         # Filtra processos que já chegaram e estão prontos para execução
#         processos_prontos = [
#             p for p in copia_processos if p.tempo_chegada <= tempo_atual
#         ]
#         if not processos_prontos:
#             # Se nenhum processo está pronto, avança o tempo para o próximo processo que chegará
#             tempo_proximo = min(p.tempo_chegada for p in copia_processos)
#             tempo_atual = tempo_proximo
#             continue

#         # Seleciona o processo com o menor tempo de execução entre os prontos
#         processo = min(processos_prontos, key=lambda p: p.tempo_execucao)

#         # Remove o processo selecionado da lista
#         copia_processos.remove(processo)

#         # Calcula o tempo de espera e turnaround
#         tempo_espera = tempo_atual - processo.tempo_chegada
#         turnaround_processo = tempo_espera + processo.tempo_execucao
#         turnaround_total += turnaround_processo
#         list_turnaround.append(turnaround_processo)
#         resultados.append(
#             {
#                 "id": processo.id,
#                 "inicio": processo.tempo_chegada,
#                 "fim": processo.tempo_execucao,
#                 "tempo_espera": tempo_espera + processo.tempo_chegada,
#                 "turnaround": turnaround_processo,
#                 "Turnaround_Medio": turnaround_total / len(processos),
#                 "tempo_chegada": processo.tempo_chegada,
#                 "tempo_execucao": processo.tempo_execucao,
#             }
#         )

#         # Imprime informações do processo
#         print(
#             f"Executando {processo} tempo_espera {tempo_espera} turnaround_processo = {turnaround_processo}"
#         )

#         # Atualiza o tempo atual após a execução do processo
#         tempo_atual += processo.tempo_execucao
#     # resultados.append(turnaround_total / qtdProcessos)
#     print(resultados)
#     return resultados


# def round_robin(processos):

#     tempo_atual = 0
#     turnaround_total = 0
#     resultados = []
#     fila_processos = []

#     dados_processos = {
#         p.id: {
#             "tempo_execucao": [],  # Lista de tuplas (inicio, fim) para cada período de execução
#             "tempo_espera": [],  # Lista de tuplas (inicio, fim) para cada período de espera
#             "turnaround": 0,
#             "sobrecarga": [],  # Lista de tuplas (inicio, fim) para cada período de sobrecarga
#             "tempo_chegada": 0,
#         }
#         for p in processos
#     }

#     while processos or fila_processos:
#         # Adiciona processos que chegaram ao tempo_atual à fila de processos
#         processos_chegaram = [p for p in processos if p.tempo_chegada <= tempo_atual]
#         for p in processos_chegaram:
#             fila_processos.append(p)
#             processos.remove(p)

#         if not fila_processos:
#             if processos:
#                 # Se não há processos prontos, avance o tempo para o próximo processo que chegará
#                 tempo_proximo = min(p.tempo_chegada for p in processos)
#                 tempo_atual = tempo_proximo
#                 continue
#             else:
#                 break

#         # Seleciona o próximo processo da fila de processos prontos
#         processo_atual = fila_processos.pop(0)
#         processo_atual.contador_execucao += 1

#         # Executa o processo atual por até o quantum ou até terminar
#         tempo_execucao = min(
#             processo_atual.quantum_sistema, processo_atual.tempo_restante
#         )
#         inicio_execucao = tempo_atual
#         fim_execucao = tempo_atual + tempo_execucao
#         for p in fila_processos:
#             if p.id != processo_atual.id:
#                 if tempo_atual > p.tempo_chegada and p.contador_execucao == 0:
#                     gap_espera = 0
#                     gap_espera = tempo_atual - p.tempo_chegada
#                     inicio_espera = tempo_atual - gap_espera
#                     dados_processos[p.id]["tempo_espera"].append(
#                         {"inicio": inicio_espera, "fim": fim_execucao}
#                     )
#                 else:
#                     inicio_espera = tempo_atual
#                     dados_processos[p.id]["tempo_espera"].append(
#                         {"inicio": inicio_espera, "fim": fim_execucao}
#                     )
#         dados_processos[processo_atual.id]["tempo_execucao"].append(
#             {"inicio": inicio_execucao, "fim": fim_execucao}
#         )

#         dados_processos[processo_atual.id][
#             "quantum_sistema"
#         ] = processo_atual.quantum_sistema

#         processo_atual.tempo_restante -= tempo_execucao
#         tempo_atual += tempo_execucao

#         if "inicio" not in dados_processos[processo_atual.id]:
#             dados_processos[processo_atual.id]["inicio"] = tempo_atual - tempo_execucao
#             dados_processos[processo_atual.id]["fim"] = tempo_atual
#             dados_processos[processo_atual.id]["id"] = processo_atual.id
#             dados_processos[processo_atual.id][
#                 "tempo_chegada"
#             ] = processo_atual.tempo_chegada

#         if processo_atual.tempo_restante > 0:
#             # Se o processo não terminou, coloque-o de volta no final da fila de prontos
#             processos.append(processo_atual)
#             sobrecarga_inicio = tempo_atual
#             tempo_atual += processo_atual.sobrecarga_sistema
#             sobrecarga_fim = tempo_atual

#             dados_processos[processo_atual.id]["sobrecarga"].append(
#                 {"inicio": sobrecarga_inicio, "fim": sobrecarga_fim}
#             )

#             dados_processos[processo_atual.id]["fim"] = tempo_atual

#             # dados_processos[processo_atual.id]["tempo_espera"].append(
#             #     {
#             #         "inicio": tempo_atual,
#             #         "fim":  tempo_execucao+tempo_atual,
#             #     }
#             # )

#         # Se o processo terminou, calcula os tempos de turnaround e espera
#         if processo_atual.tempo_restante == 0:
#             turnaround_processo = tempo_atual - processo_atual.tempo_chegada
#             tempo_espera = turnaround_processo - processo_atual.tempo_execucao
#             dados_processos[processo_atual.id]["tempo_espera"].append(
#                 {
#                     "inicio": dados_processos[processo_atual.id]["inicio"],
#                     "fim": fim_execucao,
#                 }
#             )

#             # Atualiza o dicionário do processo com os dados finais

#             dados_processos[processo_atual.id]["turnaround"] = turnaround_processo

#             # Adiciona os dados do processo aos resultados

#             resultados.append(dados_processos[processo_atual.id])

#             print(
#                 f"Processo {processo_atual.id}: tempo_espera = {tempo_espera}, turnaround_processo = {turnaround_processo} chegada {processo_atual.tempo_chegada}"
#             )

#     # Adiciona a média do turnaround aos resultados
#     media_turnaround = turnaround_total / len(processos) if processos else 0

#     print("Resultados:", resultados)
#     return resultados


# def edf(processos):
#     copia_processos = copy.deepcopy(processos)
#     tempo_atual = 0
#     turnaround_total = 0
#     resultados = []
#     lista_aux = []

#     dados_processos = {
#         p.id: {
#             "tempo_execucao": [],  # Lista de tuplas (inicio, fim) para cada período de execução
#             "tempo_espera": [],  # Lista de tuplas (inicio, fim) para cada período de espera
#             "turnaround": 0,
#             "sobrecarga": [],  # Lista de tuplas (inicio, fim) para cada período de sobrecarga
#             "tempo_chegada": p.tempo_chegada,
#             "inicio": None,
#             "fim": None,
#             "deadline": p.deadline,
#             "estouro_deadline": False,
#         }
#         for p in processos
#     }

#     while copia_processos:
#         # Filtra processos que já chegaram e estão prontos para execução
#         processos_prontos = [
#             p for p in copia_processos if p.tempo_chegada <= tempo_atual
#         ]

#         if not processos_prontos:
#             # Se nenhum processo está pronto, avança o tempo para o próximo processo que chegará
#             if copia_processos:
#                 tempo_proximo = min(p.tempo_chegada for p in copia_processos)
#                 tempo_atual = tempo_proximo
#                 continue
#             else:
#                 break

#         # Seleciona o processo com o menor tempo de deadline entre os prontos
#         processo = min(processos_prontos, key=lambda p: p.deadline)

#         if processo.tempo_restante == 0:
#             processo.tempo_restante = processo.tempo_execucao

#         inicio_execucao = tempo_atual
#         tempo_execucao = min(processo.quantum_sistema, processo.tempo_restante)
#         fim_execucao = tempo_atual + tempo_execucao

#         for p in processos_prontos:
#             if p.id != processo.id:
#                 if tempo_atual > p.tempo_chegada and p.contador_execucao == 0:
#                     gap_espera = 0
#                     gap_espera = tempo_atual - p.tempo_chegada
#                     inicio_espera = tempo_atual - gap_espera
#                     dados_processos[p.id]["tempo_espera"].append(
#                         {"inicio": inicio_espera, "fim": fim_execucao}
#                     )
#                 else:
#                     inicio_espera = tempo_atual
#                     dados_processos[p.id]["tempo_espera"].append(
#                         {"inicio": inicio_espera, "fim": fim_execucao}
#                     )

#         # Decrementa do tempo restante
#         while processo.tempo_restante > 0:
#             processo.contador_execucao += 1
#             processo.tempo_restante -= tempo_execucao
#             tempo_atual += tempo_execucao

#             dados_processos[processo.id]["tempo_execucao"].append(
#                 {"inicio": inicio_execucao, "fim": fim_execucao}
#             )
#             processos_prontos = [
#                 p for p in copia_processos if p.tempo_chegada <= tempo_atual
#             ]

#             if processos_prontos:
#                 processo_aux = min(processos_prontos, key=lambda p: p.deadline)
#                 if (
#                     tempo_atual >= processo_aux.tempo_chegada
#                     and processo.deadline > processo_aux.deadline
#                 ):
#                     if processo.tempo_chegada != 0:
#                         tempo_espera = tempo_atual - processo.tempo_execucao
#                     lista_aux.append(processo)
#                     tempo_espera_inicio = tempo_atual
#                     copia_processos.remove(processo)
#                     tempo_atual += processo.sobrecarga_sistema

#                     for p in processos_prontos:
#                         if p.id != processo.id:
#                             if (
#                                 tempo_atual > p.tempo_chegada
#                                 and p.contador_execucao == 0
#                             ):
#                                 gap_espera = 0
#                                 gap_espera = tempo_atual - p.tempo_chegada
#                                 inicio_espera = tempo_atual - gap_espera
#                                 dados_processos[p.id]["tempo_espera"].append(
#                                     {"inicio": tempo_espera_inicio, "fim": tempo_atual}
#                                 )
#                             else:
#                                 inicio_espera = tempo_atual
#                                 dados_processos[p.id]["tempo_espera"].append(
#                                     {"inicio": inicio_espera, "fim": fim_execucao}
#                                 )
#                     dados_processos[processo.id]["sobrecarga"].append(
#                         {
#                             "inicio": tempo_atual - processo.sobrecarga_sistema,
#                             "fim": tempo_atual,
#                         }
#                     )

#                     break

#             # Checa se o processo atingiu o quantum
#             if processo_aux.tempo_restante != 0:
#                 tempo_espera_inicio = tempo_atual
#                 tempo_atual += processo.sobrecarga_sistema
#                 processo.contador_quantum = 0

#                 dados_processos[processo.id]["sobrecarga"].append(
#                     {
#                         "inicio": tempo_atual - processo.sobrecarga_sistema,
#                         "fim": tempo_atual,
#                     }
#                 )
#                 for p in processos_prontos:
#                     if p.id != processo.id:
#                         if tempo_atual > p.tempo_chegada and p.contador_execucao == 0:
#                             gap_espera = 0
#                             gap_espera = tempo_atual - p.tempo_chegada
#                             inicio_espera = tempo_atual - gap_espera
#                             dados_processos[p.id]["tempo_espera"].append(
#                                 {"inicio": inicio_espera, "fim": fim_execucao}
#                             )
#                         else:
#                             inicio_espera = tempo_atual
#                             dados_processos[p.id]["tempo_espera"].append(
#                                 {"inicio": tempo_espera_inicio, "fim": tempo_atual}
#                             )
#                 dados_processos[processo.id]["tempo_execucao"].append(
#                     {"inicio": inicio_execucao, "fim": fim_execucao}
#                 )

#                 break

#         # Remove o processo selecionado da lista
#         if processo.tempo_restante == 0:
#             processos_prontos.remove(processo)
#             copia_processos.remove(processo)

#             turnaround_processo = tempo_atual - processo.tempo_chegada
#             tempo_espera = turnaround_processo - processo.tempo_execucao
#             turnaround_total += turnaround_processo

#             dados_processos[processo.id]["turnaround"] = turnaround_processo
#             dados_processos[processo.id]["tempo_execucao"].append(
#                 {"inicio": inicio_execucao, "fim": tempo_atual}
#             )
#             dados_processos[processo.id]["inicio"] = inicio_execucao
#             dados_processos[processo.id]["fim"] = tempo_atual
#             dados_processos[processo.id]["id"] = processo.id
#             if turnaround_processo > processo.deadline:
#                 dados_processos[processo.id]["estouro_deadline"] = True

#             resultados.append(dados_processos[processo.id])

#             print(
#                 f"Executando {processo} tempo_espera {tempo_espera} turnaround_processo = {turnaround_processo}"
#             )

#         # Adiciona processos pausados de volta à lista de processos
#         copia_processos.extend(lista_aux)
#         lista_aux.clear()

#     # Calcula a média de turnaround e adiciona ao resultado final

#     media_turnaround = turnaround_total / len(processos) if processos else 0
#     print(media_turnaround)
#     # Mostra os dados dos processos
#     print(resultados)

#     return resultados


# def criar_grafico_gantt(resultados, tempo_total, tipo_escalonador):
#     fig, gnt = plt.subplots()
#     resultados = sorted(resultados, key=lambda r: r["id"])
#     gnt.set_xlabel("Tempo")
#     gnt.set_ylabel("Processos")

#     y_ticks = []
#     y_labels = []

#     for idx, resultado in enumerate(resultados):
#         if "id" in resultado:
#             y_ticks.append(10 * (idx + 1))
#             y_labels.append(f"Processo {resultado['id']}")

#             if tipo_escalonador == 1:
#                 # Adiciona a barra para o tempo de espera (cor azul)
#                 if resultado["tempo_espera"] and resultado["tempo_chegada"] > 0:
#                     gnt.broken_barh(
#                         [
#                             (
#                                 resultado["inicio"],
#                                 resultado["tempo_espera"] - resultado["tempo_chegada"],
#                             )
#                         ],  # Tempo de espera
#                         (10 * idx, 9),
#                         facecolor="blue",
#                         edgecolor="black",
#                     )

#                 # Adiciona a barra para o tempo de execução (cor laranja)
#                 gnt.broken_barh(
#                     [
#                         (resultado["tempo_espera"], resultado["fim"])
#                     ],  # Tempo de execução
#                     (10 * idx, 9),
#                     facecolor="orange",
#                     edgecolor="black",
#                 )
#             elif tipo_escalonador == 2:
#                 # Visualiza o tempo de execução (cor laranja)
#                 if resultado["tempo_espera"] and resultado["tempo_chegada"] > 0:
#                     gnt.broken_barh(
#                         [
#                             (
#                                 resultado["tempo_chegada"],
#                                 resultado["inicio"],
#                             )
#                         ],  # Tempo de espera
#                         (10 * idx, 9),
#                         facecolor="blue",
#                         edgecolor="black",
#                     )
#                 for tempo_espera in resultado["tempo_espera"]:
#                     gnt.broken_barh(
#                         [
#                             (
#                                 tempo_espera["inicio"],
#                                 tempo_espera["fim"] - tempo_espera["inicio"],
#                             )
#                         ],
#                         (10 * idx, 9),
#                         facecolor="blue",
#                         edgecolor="black",
#                     )

#                 for tempo_execucao in resultado["tempo_execucao"]:
#                     gnt.broken_barh(
#                         [
#                             (
#                                 tempo_execucao["inicio"],
#                                 tempo_execucao["fim"] - tempo_execucao["inicio"],
#                             )
#                         ],
#                         (10 * idx, 9),
#                         facecolor="orange",
#                         edgecolor="black",
#                     )

#                 # Visualiza todos os períodos de sobrecarga
#                 if "sobrecarga" in resultado:
#                     for sobrecarga in resultado["sobrecarga"]:
#                         gnt.broken_barh(
#                             [
#                                 (
#                                     sobrecarga["inicio"],
#                                     sobrecarga["fim"] - sobrecarga["inicio"],
#                                 )
#                             ],
#                             (10 * idx, 9),
#                             facecolor="grey",
#                             edgecolor="black",
#                         )

#             elif tipo_escalonador == 4:

#                 # Adiciona a barra para o tempo de execução (cor laranja ou vermelha para estourar o deadline)
#                 gnt.broken_barh(
#                     [(resultado["inicio"], resultado["fim"] - resultado["inicio"])],
#                     (10 * idx, 9),
#                     facecolor=(
#                         "orange"
#                         if not resultado.get("estouro_deadline", False)
#                         else "red"
#                     ),
#                     edgecolor="black",
#                 )

#                 # Adiciona linha vertical para processos que estouraram o deadline
#                 if resultado.get("estouro_deadline", False):
#                     gnt.axvline(
#                         x=resultado["fim"], color="blue", linestyle="--", linewidth=1
#                     )
#     gnt.set_yticks(y_ticks)
#     gnt.set_yticklabels(y_labels)

#     x_ticks = range(0, tempo_total + 1)
#     gnt.set_xticks(x_ticks)
#     fig.tight_layout()
#     plt.grid(True)

#     plt.show()


# from bokeh.layouts import column


# def criar_grafico_gantt_bokeh(resultados, tipo_escalonador):

#     # Prepara os dados
#     y_labels = [f"Processo {r['id']}" for r in resultados]
#     y_positions = {label: idx for idx, label in enumerate(y_labels)}

#     # Prepara listas para os dados
#     x = []
#     y = []
#     width = []
#     height = []
#     colors = []
#     legend_labels = []

#     for resultado in resultados:
#         y_pos = y_positions[f"Processo {resultado['id']}"]

#         if tipo_escalonador in ["FIFO", "SJF"]:
#             # Tempo de espera
#             if resultado.get("tempo_espera") and resultado.get("tempo_chegada") > 0:
#                 x.append(
#                     resultado["inicio"]
#                     + (resultado["tempo_espera"] - resultado["tempo_chegada"]) / 2
#                 )
#                 y.append(y_pos)
#                 width.append(resultado["tempo_espera"] - resultado["tempo_chegada"])
#                 height.append(0.4)
#                 colors.append("blue")
#                 legend_labels.append("Tempo de Espera")

#             # Tempo de execução
#             x.append(resultado["tempo_espera"] + (resultado["tempo_execucao"]) / 2)
#             y.append(y_pos)
#             width.append(resultado["tempo_execucao"])
#             height.append(0.4)
#             colors.append("orange")
#             legend_labels.append("Tempo de Execução")

#         if tipo_escalonador == "RR":

#             for espera in resultado.get("tempo_espera", []):
#                 if resultado.get("tempo_espera") and resultado.get("tempo_chegada") > 0:
#                     x.append(
#                         resultado["tempo_chegada"]
#                         + (resultado["inicio"] - resultado["tempo_chegada"]) / 2
#                     )
#                     y.append(y_pos)
#                     width.append(resultado["inicio"] - resultado["tempo_chegada"])
#                     height.append(0.4)
#                     colors.append("blue")
#                     legend_labels.append("Tempo de Espera")
#             else:
#                 x.append(espera["inicio"] + (espera["fim"] - espera["inicio"]) / 2)
#                 y.append(y_pos)
#                 width.append(espera["fim"] - espera["inicio"])
#                 height.append(0.4)
#                 colors.append("blue")
#                 legend_labels.append("Tempo de Espera")

#             for execucao in resultado.get("tempo_execucao", []):
#                 x.append(
#                     execucao["inicio"] + (execucao["fim"] - execucao["inicio"]) / 2
#                 )
#                 y.append(y_pos)
#                 width.append(execucao["fim"] - execucao["inicio"])
#                 height.append(0.4)
#                 colors.append("orange")
#                 legend_labels.append("Tempo de Execução")

#             if "sobrecarga" in resultado and len(resultado["sobrecarga"]) > 0:
#                 for sobrecarga in resultado["sobrecarga"]:
#                     x.append(
#                         sobrecarga["inicio"]
#                         + (sobrecarga["fim"] - sobrecarga["inicio"]) / 2
#                     )
#                     y.append(y_pos)
#                     width.append(sobrecarga["fim"] - sobrecarga["inicio"])
#                     height.append(0.4)
#                     colors.append("grey")
#                     legend_labels.append("Sobrecarga")
#         if tipo_escalonador == "EDF":
#             # Tempo de execução
#             for execucao in resultado.get("tempo_execucao", []):
#                 x.append(
#                     execucao["inicio"] + (execucao["fim"] - execucao["inicio"]) / 2
#                 )
#                 y.append(y_pos)
#                 width.append(execucao["fim"] - execucao["inicio"])
#                 height.append(0.4)

#                 colors.append("orange")
#                 legend_labels.append("Tempo de Execução")

#             # Linha vertical para estourar o deadline

#             if resultado.get("estouro_deadline"):
#                 x.append(
#                     resultado["deadline"]
#                     + (resultado["fim"] - resultado["deadline"]) / 2
#                 )
#                 y.append(y_pos + 0.4)
#                 width.append(resultado["fim"] - resultado["deadline"])
#                 height.append(0.01)
#                 colors.append("red")
#                 legend_labels.append("Estouro do Deadline")

#             # Sobreposições de sobrecarga
#             if "sobrecarga" in resultado and len(resultado["sobrecarga"]) > 0:
#                 for sobrecarga in resultado["sobrecarga"]:
#                     x.append(
#                         sobrecarga["inicio"]
#                         + (sobrecarga["fim"] - sobrecarga["inicio"]) / 2
#                     )
#                     y.append(y_pos)
#                     width.append(sobrecarga["fim"] - sobrecarga["inicio"])
#                     height.append(0.4)
#                     colors.append("grey")
#                     legend_labels.append("Sobrecarga")

#             for espera in resultado.get("tempo_espera", []):
#                 x.append(espera["inicio"] + (espera["fim"] - espera["inicio"]) / 2)
#                 y.append(y_pos)
#                 width.append(espera["fim"] - espera["inicio"])
#                 height.append(0.4)
#                 colors.append("blue")
#                 legend_labels.append("Tempo de Espera")

#     titulos_escalonadores = {
#         "FIFO": "Gráfico de Gantt - Escalonador  FIFO\n Processos são executados na ordem em que chegam na fila de prontos.\n O primeiro processo a chegar é o primeiro a ser executado até a conclusão, sem interrupção.",
#         "SJF": "Gráfico de Gantt - Escalonador  SJF\n O processo com o menor tempo estimado de execução é selecionado para execução primeiro.\n Isso reduz o tempo médio de espera, mas pode causar o problema de processos mais longos sendo retardados.:",
#         "RR": "Gráfico de Gantt - Escalonador  ROUND ROBIN\n Cada processo recebe um intervalo de tempo fixo (quantum)para execução. Após o quantum,\n o processo é colocado no final da fila e o próximo processo é executado, garantindo que todos os processos recebam tempo de CPU de forma equitativa.",
#         "EDF": "Gráfico de Gantt - Escalonador  EDF\n Tarefas são escalonadas com base em seus prazos. A tarefa com o prazo mais próximo é escolhida para execução,\n garantindo que tarefas mais urgentes sejam concluídas primeiro.",
#     }
#     titulo_grafico = titulos_escalonadores.get(tipo_escalonador, "Gráfico de Gantt")
#     # Cria o ColumnDataSource
#     source = ColumnDataSource(
#         data=dict(
#             x=x,
#             y=y,
#             width=width,
#             height=height,
#             color=colors,
#             legend_label=legend_labels,
#         )
#     )

#     # Cria o gráfico
#     p = figure(
#         height=800,
#         width=1680,
#         title=titulo_grafico,
#         x_axis_label="Tempo",
#         y_axis_label="Processos",
#         y_range=FactorRange(*y_labels),
#     )

#     p.rect(
#         x="x",
#         y="y",
#         width="width",
#         height="height",
#         color="color",
#         source=source,
#         legend_field="legend_label",
#     )

#     p.y_range.factors = y_labels
#     p.yaxis.axis_label = "Processos"
#     p.xaxis.axis_label = "Tempo"
#     p.legend.title = "Legenda"
#     p.legend.location = "top_left"
#     p.x_range.start = 0

#     if tipo_escalonador == "RR":
#         titulo = "Round Robin"
#     elif tipo_escalonador == "FIFO":
#         titulo = "FIFO"
#     elif tipo_escalonador == "EDF":
#         titulo = "EDF"
#     elif tipo_escalonador == "SJF":
#         titulo = "SJF"

#     output_file("grafico_gantt.html", title=titulo)

#     show(p)


# def main():
#     quantum_sistema = 2
#     sobrecarga_sistema = 1

#     # lista_processos = [
#     #     Processo(1, 5, 1, 6, quantum_sistema, sobrecarga_sistema),
#     #     Processo(2, 1, 5, 12, quantum_sistema, sobrecarga_sistema),
#     #     Processo(3, 2, 7, 8, quantum_sistema, sobrecarga_sistema),
#     #     Processo(4, 3, 3, 4, quantum_sistema, sobrecarga_sistema),
#     # ]
#     lista_processos = [
#         Processo(1, 0, 15, 45, quantum_sistema, sobrecarga_sistema),
#         Processo(2, 3, 4, 9, quantum_sistema, sobrecarga_sistema),
#         Processo(3, 6, 10, 10, quantum_sistema, sobrecarga_sistema),
#         Processo(4, 9, 10, 35, quantum_sistema, sobrecarga_sistema),
#     ]

#     # lista_processos = [
#     #     Processo(1, 0, 4, 7, quantum_sistema, sobrecarga_sistema),
#     #     Processo(2, 2, 2, 5, quantum_sistema, sobrecarga_sistema),
#     #     Processo(3, 4, 1, 8, quantum_sistema, sobrecarga_sistema),
#     #     Processo(4, 6, 3, 10, quantum_sistema, sobrecarga_sistema),
#     # ]
#     # self, id, tempo_chegada, tempo_execucao, deadline, quantum_sistema, sobrecarga_sistema, paginas
#     # lista_processos = [
#     #     Processo(1, 0, 1, 6, quantum_sistema, sobrecarga_sistema),
#     #     Processo(2, 0, 5, 12, quantum_sistema, sobrecarga_sistema),
#     #     Processo(3, 0, 7, 8, quantum_sistema, sobrecarga_sistema),
#     #     Processo(4, 0, 3, 4, quantum_sistema, sobrecarga_sistema),
#     # ]

#     # print("FIFO:")
#     # fifo_resultado = fifo(lista_processos)
#     # criar_grafico_gantt_bokeh(fifo_resultado, 1)
#     # criar_grafico_gantt_bokeh(fifo_resultado, 1)
#     # print("\nSJF:")
#     # sjf_resultado=sjf(lista_processos[:])
#     # criar_grafico_gantt_bokeh(sjf_resultado,2)

#     print("\nRound Robin:")
#     rr_resultado = round_robin(lista_processos)

#     criar_grafico_gantt_bokeh(rr_resultado, "RR")

#     # print("\nEDF:")
#     # edf1= edf(lista_processos[:])
#     # criar_grafico_gantt_bokeh(edf1, 4)


# if __name__ == "__main__":
#     main()
