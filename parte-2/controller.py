import copy
from fastapi import APIRouter, Body
from service.plotagem import criar_grafico_gantt_bokeh
from service.fifo import fifo
from service.edf import edf
from service.rr import round_robin
from service.sjf import sjf
from models import *

router = APIRouter()

# Rota para o método GET

list = []


@router.post("/newprocess")
async def get_escalonador(process: ProcessoModel = Body(...)):

    process.id = len(list) + 1
    list.append(process)

    return {"message": "processo inserted successfully", "process": list}


@router.get("/getprocesslist")
async def get_process_list():
    if len(list) != 0:
        return {"process": list}


@router.post("/creategraph")
async def create_graph(request: GraphRequest):
    tipo_escalonador = request.tipo_escalonador
    if (tipo_escalonador== 'FIFO'):
        processos = copy.deepcopy(list)
        processo, turnaround = fifo(processos)
        plot = criar_grafico_gantt_bokeh(processo, tipo_escalonador)
        
        return plot, turnaround
    
    if (tipo_escalonador== 'SJF'):
        processos = copy.deepcopy(list)
        processo, turnaround = sjf(processos)
        plot = criar_grafico_gantt_bokeh(processo, tipo_escalonador)
        
        return plot, turnaround
    
    if (tipo_escalonador== 'RR'):
        print(tipo_escalonador)
        processos = copy.deepcopy(list)
        processo, turnaround = round_robin(processos)
        for item in processo:
            print(item)
        plot = criar_grafico_gantt_bokeh(processo, tipo_escalonador)
        
        return plot, turnaround
    
    if (tipo_escalonador == 'EDF'):
        print(tipo_escalonador)
        processos = copy.deepcopy(list)
        processo, turnaround = edf(processos)
        plot = criar_grafico_gantt_bokeh(processo,tipo_escalonador)
        
        return plot, turnaround
    
@router.post("/clear")
async def limpara_lista():
    global list
    list = []  # Limpa a lista de processos
    return "ok"
