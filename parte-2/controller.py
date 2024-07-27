from fastapi import Body
from aplication import *
from fastapi import APIRouter,HTTPException
from models import*
import matplotlib.pyplot as plt
import numpy as np
from fastapi.middleware.cors import CORSMiddleware
import io
import base64


router = APIRouter()

# Rota para o método GET
list=[]

@router.post("/newprocess")
async def get_escalonador(process: ProcessoModel = Body(...) ):
   
    if len(list)!=0:
        primeiro_processo=list[0]
        process.quantum_sistema=primeiro_processo.quantum_sistema
        process.sobrecarga_sistema=primeiro_processo.sobrecarga_sistema
    process.id = len(list)+1
    list.append(process)

    
    return {"message": "processo inserted successfully", "process": list}


@router.get("/getprocesslist")
async def get_process_list():
    return {"process": list}

    
    return {"message": "processo inserted successfully", "process": list}

@router.post("/creategraph")
async def get_graph():
    fig, ax = plt.subplots(figsize=(10, 6))
    
    y_ticks = []
    y_labels = []

    for idx, processo in enumerate(list):
        y_ticks.append(10 * (idx + 1))
        y_labels.append(f'Processo {processo.id}')
        ax.broken_barh([(processo.tempo_chegada, processo.tempo_execucao)], (10 * idx, 9))

    ax.set_yticks(y_ticks)
    ax.set_yticklabels(y_labels)
    ax.set_xlabel('Tempo')
    ax.set_ylabel('Processos')
    ax.grid(True)
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    plt.close(fig)

    return {"image": image_base64}




 
