from passlib.hash import pbkdf2_sha256
from jose import jwt
from datetime import datetime, timedelta
SECRET_KEY = "ProtectoSiniestros"
ALGORITHM = "HS256"

def crear_token(data):
    data["exp"]=datetime.utcnow() + timedelta(minutes=10)
    token = jwt.encode(claims = data, key = SECRET_KEY, algorithm = ALGORITHM)
    return token
def verificar_token(token):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload
def hash_contrasenya(contrasenya):
    return pbkdf2_sha256.hash(contrasenya)
def verificar_contrasenya(contrasenya, hash_contrasenya):
    return pbkdf2_sha256.verify(contrasenya, hash_contrasenya)