from pydantic import BaseModel
from typing import List

class ProcessoModel(BaseModel):
    id: int
    tempo_chegada: float
    tempo_execucao: float
    deadline: float
    quantum_sistema: float
    sobrecarga_sistema: float
    tempo_restante: float
    paginas_na_ram: List[int] = []
 

