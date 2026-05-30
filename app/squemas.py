from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator

class CreateUserRequest(BaseModel):
    name: str
    password: str

    @field_validator('password')
    def password_minimo(cls, v):
        if len(v) < 8:
            raise ValueError('La contraseña debe tener al menos 8 caracteres')
        return v
    
class ClasificarRequest(BaseModel):
    descripcion: str
    usar_rag: bool = True
    

    @field_validator('descripcion')
    def descripcion_maximo(cls, v):
        if len(v) > 150:
            raise ValueError('La descripción debe tener como maximo 150 caracteres')
        return v