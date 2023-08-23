from sqlalchemy import create_engine, Column, Integer, Float, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Skaiciavimas(Base):
    __tablename__ = 'skaiciavimai'

    id = Column(Integer, primary_key=True)
    skaiciu_seka = Column(String)
    rezultatas = Column(Float)

def init_db():
    engine = create_engine('sqlite:///skaiciavimai.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()

def saugoti_skaiciavima(session, seka, rezultatas):
        skaiciavimas1 = Skaiciavimas(skaiciu_seka=' '.join(seka), rezultatas=rezultatas)
        session.add(skaiciavimas1)
        session.commit()
def gauti_istorija(session):
    return session.query(Skaiciavimas).all()


