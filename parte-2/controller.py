from fastapi import APIRouter, Body

from aplication import *
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
        processo = fifo(processos)
        plot = criar_grafico_gantt_bokeh(processo, tipo_escalonador)
        
        return plot
    if (tipo_escalonador== 'SJF'):
        processos = copy.deepcopy(list)
        processo = sjf(processos)
        plot = criar_grafico_gantt_bokeh(processo, tipo_escalonador)
        
        return plot
    if (tipo_escalonador== 'RR'):
        print(tipo_escalonador)
        processos = copy.deepcopy(list)
        processo = round_robin(processos)
        for item in processo:
            print(item)
        plot = criar_grafico_gantt_bokeh(processo, tipo_escalonador)
        
        return plot
    if (tipo_escalonador== 'EDF'):
        print(tipo_escalonador)
        processos = copy.deepcopy(list)
        processo=edf(processos)
        plot=criar_grafico_gantt_bokeh(processo,tipo_escalonador)
        return plot

    
