from app.database import Base
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime

class Siniestro(Base):
    __tablename__ = "siniestros"

    id = Column(Integer, primary_key=True, index=True)
    gremio_real = Column(String)
    garantia_real = Column(String)
    gremio_predicho  = Column(String)
    garantia_predicha = Column(String)
    descripcion = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)