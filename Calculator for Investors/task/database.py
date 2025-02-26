import os

from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import pandas as pd

Base = declarative_base()

class Companies(Base):
    __tablename__ = 'companies'

    ticker = Column(String(10), primary_key=True)
    name = Column(String(100))
    sector = Column(String(100))

class Financial(Base):
    __tablename__ = 'financial'

    ticker = Column(String(10), primary_key=True)
    ebitda = Column(Integer)
    sales = Column(Integer)
    net_profit = Column(Integer)
    market_price = Column(Integer)
    net_debt = Column(Integer)
    assets = Column(Integer)
    equity = Column(Integer)
    cash_equivalents = Column(Integer)
    liabilities = Column(Integer)

class Database():
    def __init__(self):
        engine = create_engine("sqlite:///investor.db", echo=False)
        Base.metadata.create_all(bind=engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

        self.add_companies()
        self.add_financial()

    def add_companies(self):
        path = os.getcwd() + "\\companies.csv"
        df = pd.read_csv(os.getcwd() + "\\companies.csv")
        self.session.query(Companies).delete()
        self.session.commit()

        for index, row in df.iterrows():
            company = Companies(ticker=row["ticker"], name=row["name"], sector=row["sector"])
            self.session.add(company)

        self.session.commit()

    def add_financial(self):
        df = pd.read_csv(os.getcwd() + "\\financial.csv")
        self.session.query(Financial).delete()
        self.session.commit()
        for index, row in df.iterrows():
            financial = Financial(ticker=row["ticker"], ebitda=row["ebitda"], sales=row["sales"],
                                  net_profit=row["net_profit"], market_price=row["market_price"],
                                  net_debt=row["net_debt"], assets=row["assets"], equity=row["equity"],
                                  cash_equivalents=row["cash_equivalents"], liabilities=row["liabilities"])
            self.session.add(financial)
        self.session.commit()






