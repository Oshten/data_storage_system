from sqlalchemy import Column, Integer, Date, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class Data(Base):
    __tablename__ = 'datas'
    id = Column(Integer, primary_key=True)
    date = Column(Date())
    company = Column(String(12))
    type = Column(String(4))
    fact = Column(Integer)
    forecast = Column(Integer)

    def __str__(self):
        return f'{self.id} {self.date}. Company: {self.company} - {self.type}'

    def __repr__(self):
        return str(self)