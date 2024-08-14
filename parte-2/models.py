from typing import List, Optional

from pydantic import BaseModel, model_validator


class ProcessoModel(BaseModel):
    id: Optional[int] = None
    tempo_chegada: float
    tempo_execucao: float
    deadline: float
    quantum_sistema: Optional[int] = None
    sobrecarga_sistema: Optional[int] = None
    paginas_na_ram: List[int] = []

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
