from fastapi import Body
from aplication import *
from fastapi import APIRouter,HTTPException
from models import*


router = APIRouter()
# Rota para o método GET
list=[]

@router.post("/newprocess")
async def get_escalonador(process: ProcessoModel = Body(...)):
    process.id = len(list)+1
    list.append(process)
    
    return {"message": "processo inserted successfully", "process": list}





 
