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
    
@router.post("/clear")
async def limpara_lista():
    global list
    list = []  # Limpa a lista de processos
    return "ok"


@router.post("/getturnaroundlist")
async def calcturnaround():
        turnaroundList=[]
        processos = copy.deepcopy(list)
        processo_fifo = fifo(processos)
        processo_edf=edf(processos)
        processo_sjf=sjf(processos)
        processo_rr=round_robin(processos)
        turnaroundmedio_fifo= processo_fifo[-1]["turnaroundmedio"]
        turnaroundmedio_edf= processo_edf[-1]["turnaroundmedio"]
        turnaroundmedio_sjf= processo_sjf[-1]["turnaroundmedio"]
        turnaroundmedio_rr= processo_rr[-1]["turnaroundmedio"]
        turnaroundList.extend([turnaroundmedio_fifo,turnaroundmedio_sjf,turnaroundmedio_rr,turnaroundmedio_edf])
        return turnaroundList
        
        

