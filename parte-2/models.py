import string
from typing import List, Optional

from pydantic import BaseModel, Field, model_validator


class ProcessoModel(BaseModel):
    id: Optional[int] = None
    tempo_chegada: float
    tempo_execucao: float
    deadline: float
    quantum_sistema: Optional[int] = None
    sobrecarga_sistema: Optional[int] = None
    tempo_restante: float = Field(default=None)
    contador_quantum: int = Field(default=0)
    contador_execucao:int = Field(default=0)

    

    def __init__(self, **data):
        super().__init__(**data)
        # Se tempo_restante não for fornecido, inicialize com tempo_execucao
        if self.tempo_restante is None:
            self.tempo_restante = self.tempo_execucao

    @model_validator(mode="before")
    def convert_values(cls, values):
        for field in ["quantum_sistema", "sobrecarga_sistema"]:
            value = values.get(field)
            if isinstance(value, str):
                if value.strip() == "":
                    values[field] = 0
                else:
                    try:
                        values[field] = int(value)
                    except ValueError:
                        values[field] = None
            elif value is None:
                values[field] = 0
        return values


class GraphRequest(BaseModel):
    tipo_escalonador: str