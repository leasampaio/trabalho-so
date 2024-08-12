import copy
import time
import matplotlib.pyplot as plt
import numpy as np
from typing import List


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
                f"tempo_restante={self.tempo_restante}")
    
 
    
        
        
def fifo(processos:Processo):
    tempo_atual = 0
    resultados = []
    turnaround_total=0
    # Ordena os processos pelo tempo de chegada
    processos_ordenados = sorted(processos, key=lambda p: p.tempo_chegada)

    for processo in processos_ordenados:
        # Atualiza o tempo atual se for menor que o tempo de chegada do process
        if tempo_atual < processo.tempo_chegada:
            tempo_atual = processo.tempo_chegada

        # Calcula o tempo de espera e o turnaround do processo
        tempo_espera = tempo_atual - processo.tempo_chegada
        turnaround_processo = tempo_espera + processo.tempo_execucao
        turnaround_total+=turnaround_processo
       
        # Adiciona os resultados à lista
        resultados.append((tempo_espera, turnaround_processo))
        print(f"Executando {processo} tempo_espera {tempo_espera} turnaround_processo = {turnaround_processo}")

        # Atualiza o tempo atual após a execução do processo
        tempo_atual += processo.tempo_execucao 
    resultados.append(turnaround_total/len(processos)) 
    print(f"turnaround_total = {turnaround_total}")
        
    print(resultados)
    return resultados
    
 


def sjf(processos):
    tempo_atual = 0
    resultados = []
    list_turnaround = []
    turnaround_total=0
    qtdProcessos=len(processos)

    
    while processos:
        # Filtra processos que já chegaram e estão prontos para execução
        processos_prontos = [p for p in processos if p.tempo_chegada <= tempo_atual]
        if not processos_prontos:
            # Se nenhum processo está pronto, avança o tempo para o próximo processo que chegará
            tempo_proximo = min(p.tempo_chegada for p in processos)
            tempo_atual = tempo_proximo
            continue
        
        # Seleciona o processo com o menor tempo de execução entre os prontos
        processo = min(processos_prontos, key=lambda p: p.tempo_execucao)
        
        # Remove o processo selecionado da lista
        processos.remove(processo)
        
        # Calcula o tempo de espera e turnaround
        tempo_espera = tempo_atual - processo.tempo_chegada
        turnaround_processo = tempo_espera + processo.tempo_execucao
        turnaround_total+=turnaround_processo
        list_turnaround.append(turnaround_processo)
        resultados.append((tempo_espera, turnaround_processo))
        
        # Imprime informações do processo
        print(f"Executando {processo} tempo_espera {tempo_espera} turnaround_processo = {turnaround_processo}")

        # Atualiza o tempo atual após a execução do processo
        tempo_atual += processo.tempo_execucao
    resultados.append(turnaround_total/qtdProcessos) 
    print(resultados)
    return resultados


def round_robin(processos):
     
    fila = processos[:]
    tempo_atual = 0

    while fila:
        processo = fila.pop(0)
        if tempo_atual < processo.tempo_chegada:
            tempo_atual = processo.tempo_chegada
        
        tempo_executado = min(processo.tempo_restante, processo.quantum_sistema)
        processo.tempo_restante -= tempo_executado
        print(f"Executando {processo} no tempo {tempo_atual}")
        tempo_atual += tempo_executado + processo.sobrecarga_sistema

        if processo.tempo_restante > 0:
            fila.append(processo)

     
         


def edf(processos):
    tempo_atual = 0
    turnaround_total=0
    resultados = []
    qtdProcessos=len(processos)
    lista_aux=[]
    
    while processos or lista_aux:
        # Filtra processos que já chegaram e estão prontos para execução
        processos_prontos = [p for p in processos if p.tempo_chegada <= tempo_atual]
        processos_prontos_aux=processos_prontos
        if not processos_prontos:
            # Se nenhum processo está pronto, avança o tempo para o próximo processo que chegará
            tempo_proximo = min(p.tempo_chegada for p in processos)
            tempo_atual = tempo_proximo

            continue
        # Seleciona o processo com o menor tempo de deadline entre os prontos
        processo = min(processos_prontos, key=lambda p: p.deadline)

        processo.tempo_restante=processo.tempo_execucao
        while(processo.tempo_restante>0):
            tempo_atual+=1
            processo.tempo_restante-=1
            processos_prontos = [p for p in processos if p.tempo_chegada <= tempo_atual]
            
        
           
           # print(f"Executando {processo} ")
            if processos_prontos:
                processo_aux = min(processos_prontos, key=lambda p: p.deadline)
                #print(processo_aux)
                #print(processo)
                if tempo_atual>=processo_aux.tempo_chegada and processo.deadline > processo_aux.deadline:
                    #print(processo)
                    #print(tempo_atual)
                    lista_aux.append(processo)
                    processos.remove(processo)
                    tempo_atual += processo.sobrecarga_sistema
                    break
            
            else:
                # Caso não haja processos prontos, continue executando o processo atual
                continue
           
        # Remove o processo selecionado da lista
            #print(tempo_atual)

        
        if processo.tempo_restante == 0:
            processos.remove(processo)
           
            turnaround_processo = tempo_atual - processo.tempo_chegada
            tempo_espera =  turnaround_processo-processo.tempo_execucao
            turnaround_total += turnaround_processo
            resultados.append((tempo_espera, turnaround_processo))
            #print(tempo_atual)
            print(f"Executando {processo} tempo_espera {tempo_espera} turnaround_processo = {turnaround_processo}")

        # Adiciona processos pausados de volta à lista de processos
        processos.extend(lista_aux)
        lista_aux.clear()
        
         
        
    resultados.append(turnaround_total/qtdProcessos) 

    print(resultados)
    return resultados



def criar_grafico_gantt(processos, tempo_total):
    fig, gnt = plt.subplots()

    gnt.set_xlabel('Tempo')
    gnt.set_ylabel('Processos')

    y_ticks = []
    y_labels = []

    for idx, processo in enumerate(processos):
        y_ticks.append(10 * (idx + 1))
        y_labels.append(f'Processo {processo.id}')
        gnt.broken_barh([(processo.tempo_chegada, processo.tempo_execucao)], (10 * idx, 9))

    gnt.set_yticks(y_ticks)
    gnt.set_yticklabels(y_labels)
    gnt.grid(True)

    plt.show()

def criar_grafico_memoria(ram, disco):
    fig, ax = plt.subplots(2, 1, figsize=(10, 8))

    ax[0].barh(range(len(ram)), [x[1] for x in ram], color='blue')
    ax[0].set_yticks(range(len(ram)))
    ax[0].set_yticklabels([f'P{p[0]}-Pag{p[1]}' for p in ram])
    ax[0].set_title('RAM')

    ax[1].barh(range(len(disco)), [x[1] for x in disco], color='red')
    ax[1].set_yticks(range(len(disco)))
    ax[1].set_yticklabels([f'P{p[0]}-Pag{p[1]}' for p in disco])
    ax[1].set_title('Disco')

    plt.tight_layout()
    plt.show()


def main():
    quantum_sistema = 2
    sobrecarga_sistema = 1
    tempo_acesso_disco = 2  # Unidades de tempo para acesso ao disco

    lista_processos = [
        Processo(1, 5, 1, 6, quantum_sistema, sobrecarga_sistema),
        Processo(2, 1, 5, 12, quantum_sistema, sobrecarga_sistema),
        Processo(3, 2, 7, 8, quantum_sistema, sobrecarga_sistema),
        Processo(4, 3, 3, 4, quantum_sistema, sobrecarga_sistema),
    ]
    #self, id, tempo_chegada, tempo_execucao, deadline, quantum_sistema, sobrecarga_sistema, paginas
    # lista_processos = [
    #     Processo(1, 0, 1, 6, quantum_sistema, sobrecarga_sistema),
    #     Processo(2, 0, 5, 12, quantum_sistema, sobrecarga_sistema),
    #     Processo(3, 0, 7, 8, quantum_sistema, sobrecarga_sistema),
    #     Processo(4, 0, 3, 4, quantum_sistema, sobrecarga_sistema),
    # ]
     

    print("FIFO:")
    fifo(lista_processos[:])

    print("\nSJF:")
    sjf(lista_processos[:])

    print("\nRound Robin:")
    round_robin(lista_processos[:])

    print("\nEDF:")
    edf(lista_processos[:])

    # criar_grafico_gantt(lista_processos, 20)
    # criar_grafico_memoria(memoria.ram, memoria.disco)

if __name__ == "__main__":
    main()
