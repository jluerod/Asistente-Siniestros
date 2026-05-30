from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.database import get_db, init_db
from app.auth import *
from app.models import *
from app.squemas import *
from fastapi import HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.conversation import clasificar_siniestro
security = HTTPBearer()

def get_current_user(token: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = verificar_token(token.credentials)
        return payload
    except Exception as e:
        print(f"Error verificando token: {e}")
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

@app.post("/registro")
def create_user(user: CreateUserRequest, db: Session = Depends(get_db)):
    hash_password = hash_contrasenya(user.password)
    if db.query(Usuario).filter(Usuario.user_name==user.name).first():
        raise HTTPException(status_code=400, detail="El usuario ya existe")
    nuevo_usuario = Usuario(user_name=user.name, hashed_password=hash_password, role="user")
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return {"token": crear_token({"sub":nuevo_usuario.user_name, "role": nuevo_usuario.role})}

@app.post("/login")
def login_user(user: CreateUserRequest, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.user_name==user.name).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if not verificar_contrasenya(user.password, usuario.hashed_password):
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")
    return {"token": crear_token({"sub":usuario.user_name, "role": usuario.role})}
    
@app.post("/clasificar")
def clasificar(request: ClasificarRequest, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    resultado, _ = clasificar_siniestro(request.descripcion, request.usar_rag)
    nuevo = Siniestro(
        descripcion=request.descripcion,
        gremio_predicho=resultado['gremio'],
        garantia_predicha=resultado['garantia']
    )
    db.add(nuevo)
    db.commit()

    return resultado

