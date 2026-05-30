from app.database import Base
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean

class Siniestro(Base):
    __tablename__ = "siniestros"

    id = Column(Integer, primary_key=True, index=True)
    gremio_real = Column(String)
    garantia_real = Column(String)
    gremio_predicho  = Column(String)
    garantia_predicha = Column(String)
    descripcion = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, unique=True)
    hashed_password = Column(String)
    role  = Column(String)
    activo = Column(Boolean, default=True)
    timestamp = Column(DateTime, default=datetime.utcnow)