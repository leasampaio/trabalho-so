from bokeh.plotting import figure, show
from bokeh.io import output_file, save
from bokeh.models import ColumnDataSource, FactorRange


def criar_grafico_gantt_bokeh(resultados, tipo_escalonador):

    # Prepara os dados
    y_labels = [f"Processo {r['id']}" for r in resultados]
    y_positions = {label: idx for idx, label in enumerate(y_labels)}

    # Prepara listas para os dados
    x = []
    y = []
    width = []
    height = []
    colors = []
    legend_labels = []

    for resultado in resultados:
        y_pos = y_positions[f"Processo {resultado['id']}"]

        if tipo_escalonador in ["FIFO", "SJF"]:
            # Tempo de espera
            if resultado.get("tempo_espera") and resultado.get("tempo_chegada") > 0:
                x.append(
                    resultado["inicio"]
                    + (resultado["tempo_espera"] - resultado["tempo_chegada"]) / 2
                )
                y.append(y_pos)
                width.append(resultado["tempo_espera"] - resultado["tempo_chegada"])
                height.append(0.4)
                colors.append("blue")
                legend_labels.append("Tempo de Espera")

            # Tempo de execução
            x.append(resultado["tempo_espera"] + (resultado["tempo_execucao"]) / 2)
            y.append(y_pos)
            width.append(resultado["tempo_execucao"])
            height.append(0.4)
            colors.append("orange")
            legend_labels.append("Tempo de Execução")

        if tipo_escalonador == "RR":
            if resultado.get("tempo_espera") and resultado.get("tempo_chegada") > 0:
                x.append(
                    resultado["tempo_chegada"]
                    + (resultado["inicio"] - resultado["tempo_chegada"]) / 2
                )
                y.append(y_pos)
                width.append(resultado["inicio"] - resultado["tempo_chegada"])
                height.append(0.4)
                colors.append("blue")
                legend_labels.append("Tempo de Espera")

            for espera in resultado.get("tempo_espera", []):
                x.append(espera["inicio"] + (espera["fim"] - espera["inicio"]) / 2)
                y.append(y_pos)
                width.append(espera["fim"] - espera["inicio"])
                height.append(0.4)
                colors.append("blue")
                legend_labels.append("Tempo de Espera")

            for execucao in resultado.get("tempo_execucao", []):
                x.append(
                    execucao["inicio"] + (execucao["fim"] - execucao["inicio"]) / 2
                )
                y.append(y_pos)
                width.append(execucao["fim"] - execucao["inicio"])
                height.append(0.4)
                colors.append("orange")
                legend_labels.append("Tempo de Execução")

            if "sobrecarga" in resultado and len(resultado["sobrecarga"]) > 0:
                for sobrecarga in resultado["sobrecarga"]:
                    x.append(
                        sobrecarga["inicio"]
                        + (sobrecarga["fim"] - sobrecarga["inicio"]) / 2
                    )
                    y.append(y_pos)
                    width.append(sobrecarga["fim"] - sobrecarga["inicio"])
                    height.append(0.4)
                    colors.append("grey")
                    legend_labels.append("Sobrecarga")
        if tipo_escalonador == "EDF":
            # Tempo de execução
            for execucao in resultado.get("tempo_execucao", []):
                x.append(
                    execucao["inicio"] + (execucao["fim"] - execucao["inicio"]) / 2
                )
                y.append(y_pos)
                width.append(execucao["fim"] - execucao["inicio"])
                height.append(0.4)

                colors.append("orange")
                legend_labels.append("Tempo de Execução")

            # Linha vertical para estourar o deadline

            if resultado.get("estouro_deadline"):
                x.append(
                    resultado["deadline"]
                    + (resultado["fim"] - resultado["deadline"]) / 2
                )
                y.append(y_pos + 0.4)
                width.append(resultado["fim"] - resultado["deadline"])
                height.append(0.01)
                colors.append("red")
                legend_labels.append("Estouro do Deadline")

            # Sobreposições de sobrecarga
            if "sobrecarga" in resultado and len(resultado["sobrecarga"]) > 0:
                for sobrecarga in resultado["sobrecarga"]:
                    x.append(
                        sobrecarga["inicio"]
                        + (sobrecarga["fim"] - sobrecarga["inicio"]) / 2
                    )
                    y.append(y_pos)
                    width.append(sobrecarga["fim"] - sobrecarga["inicio"])
                    height.append(0.4)
                    colors.append("grey")
                    legend_labels.append("Sobrecarga")

            for espera in resultado.get("tempo_espera", []):
                x.append(espera["inicio"] + (espera["fim"] - espera["inicio"]) / 2)
                y.append(y_pos)
                width.append(espera["fim"] - espera["inicio"])
                height.append(0.4)
                colors.append("blue")
                legend_labels.append("Tempo de Espera")

    titulos_escalonadores = {
        "FIFO": "Gráfico de Gantt - Escalonador  FIFO\n Processos são executados na ordem em que chegam na fila de prontos.\n O primeiro processo a chegar é o primeiro a ser executado até a conclusão, sem interrupção.",
        "SJF": "Gráfico de Gantt - Escalonador  SJF\n O processo com o menor tempo estimado de execução é selecionado para execução primeiro.\n Isso reduz o tempo médio de espera, mas pode causar o problema de processos mais longos sendo retardados.:",
        "RR": "Gráfico de Gantt - Escalonador  ROUND ROBIN\n Cada processo recebe um intervalo de tempo fixo (quantum)para execução. Após o quantum,\n o processo é colocado no final da fila e o próximo processo é executado, garantindo que todos os processos recebam tempo de CPU de forma equitativa.",
        "EDF": "Gráfico de Gantt - Escalonador  EDF\n Tarefas são escalonadas com base em seus prazos. A tarefa com o prazo mais próximo é escolhida para execução,\n garantindo que tarefas mais urgentes sejam concluídas primeiro.",
    }
    titulo_grafico = titulos_escalonadores.get(tipo_escalonador, "Gráfico de Gantt")
    # Cria o ColumnDataSource
    source = ColumnDataSource(
        data=dict(
            x=x,
            y=y,
            width=width,
            height=height,
            color=colors,
            legend_label=legend_labels,
        )
    )

    # Cria o gráfico
    p = figure(
        height=800,
        width=1680,
        title=titulo_grafico,
        x_axis_label="Tempo",
        y_axis_label="Processos",
        y_range=FactorRange(*y_labels),
    )

    p.rect(
        x="x",
        y="y",
        width="width",
        height="height",
        color="color",
        source=source,
        legend_field="legend_label",
    )

    p.y_range.factors = y_labels
    p.yaxis.axis_label = "Processos"
    p.xaxis.axis_label = "Tempo"
    p.legend.title = "Legenda"
    p.legend.location = "top_left"
    p.x_range.start = 0

    if tipo_escalonador == "RR":
        titulo = "Round Robin"
    elif tipo_escalonador == "FIFO":
        titulo = "FIFO"
    elif tipo_escalonador == "EDF":
        titulo = "EDF"
    elif tipo_escalonador == "SJF":
        titulo = "SJF"

    output_file("grafico_gantt.html", title=titulo)

    show(p)
