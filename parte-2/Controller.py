from fastapi import Body
from aplication import *
from fastapi import APIRouter,HTTPException
from models import*


router = APIRouter()
# Rota para o método GET
lista=[]

@router.post("/escalonador")
async def get_escalonador(processo: ProcessoModel = Body(...)):
    processo.id = len(lista)+1
    lista.append(processo)
    
    return {"message": "processo inserted successfully", "user": lista}
   

 
