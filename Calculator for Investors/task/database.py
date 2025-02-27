import os

from sqlalchemy import Column, String, Integer, create_engine, func
from sqlalchemy.orm import declarative_base, sessionmaker
import pandas as pd
from state import State

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

    def get_calculation(self, a: float, b: float) -> str:
        try:
            x = a / b
        except Exception:
            return None
        return str(round(x, 2))

    def get_PE(self):
        return self.get_calculation(self.market_price, self.net_profit)

    def get_PS(self):
        return self.get_calculation(self.market_price, self.sales)

    def get_PB(self):
        return self.get_calculation(self.market_price, self.assets)

    def get_NB_EBITDA(self):
        return self.get_calculation(self.net_debt, self.ebitda)

    def get_NB_EBITDA_num(self):
        if not self.net_debt or not self.ebitda: return 0
        return self.net_debt / self.ebitda

    def get_ROE(self):
        return self.get_calculation(self.net_profit, self.equity)

    def get_ROE_num(self):
        if not self.net_profit or not self.equity: return 0
        return self.net_profit / self.equity

    def get_ROA(self):
        return self.get_calculation(self.net_profit, self.assets)

    def get_ROA_num(self):
        if not self.net_profit or not self.assets: return 0
        return self.net_profit / self.assets

    def get_LA(self):
        return self.get_calculation(self.liabilities, self.assets)

class Database():
    def __init__(self):
        db_file = "investor.db"
        statusnew = not os.path.exists(db_file)
        engine = create_engine(f"sqlite:///{db_file}", echo=False)
        Base.metadata.create_all(bind=engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

        if statusnew:
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

    def create_company(self):
        company = Companies()
        finance = Financial()
        company.ticker = input("Enter ticker (in the format 'MOON'):\n")
        finance.ticker = company.ticker
        company.name = input("Enter company (in the format 'Moon Corp'):\n")
        company.sector = input("Enter industries (in the format 'Technology'):\n")
        finance.ebitda = int(input("Enter ebitda (in the format '987654321'):\n"))
        finance.sales = int(input("Enter sales (in the format '987654321'):\n"))
        finance.net_profit = int(input("Enter net profit (in the format '987654321'):\n"))
        finance.market_price = int(input("Enter market price (in the format '987654321'):\n"))
        finance.net_debt = int(input("Enter net debt (in the format '987654321'):\n"))
        finance.assets = int(input("Enter assets (in the format '987654321'):\n"))
        finance.equity = int(input("Enter equity (in the format '987654321'):\n"))
        finance.cash_equivalents = int(input("Enter cash equivalents (in the format '987654321'):\n"))
        finance.liabilities = int(input("Enter liabilities (in the format '987654321'):\n"))

        self.session.add(company)
        self.session.add(finance)
        self.session.commit()
        print("Company created successfully!")
        return State.MAIN_MENU

    def read_company(self):
        name = input("Enter company name:\n")
        
        companies = self.session.query(Companies).filter(Companies.name.like(f"%{name}%")).all()
        if not companies:
            print("Company not found!")
            return State.MAIN_MENU
        else:
            for index, company in enumerate(companies):
                print(f"{index} {company.name}")
            chosen_index = int(input("Enter company number:\n"))
            ticker = companies[chosen_index].ticker
            financial = self.session.query(Financial).filter(Financial.ticker == ticker).first()
            print(f"{ticker} {companies[chosen_index].name}")
            print(f"P/E = {financial.get_PE()}")
            print(f"P/S = {financial.get_PS()}")
            print(f"P/B = {financial.get_PB()}")
            print(f"ND/EBITDA = {financial.get_NB_EBITDA()}")
            print(f"ROE = {financial.get_ROE()}")
            print(f"ROA = {financial.get_ROA()}")
            print(f"L/A = {financial.get_LA()}")
            return State.MAIN_MENU

    def update_company(self):
        name = input("Enter company name:\n")


        companies = self.session.query(Companies).filter(Companies.name.like(f"%{name}%")).all()
        if not companies:
            print("Company not found!")
            return State.MAIN_MENU
        else:
            for index, company in enumerate(companies):
                print(f"{index} {company.name}")
            chosen_index = int(input("Enter company number:\n"))
            ticker = companies[chosen_index].ticker
            finance = self.session.query(Financial).filter(Financial.ticker == ticker).first()
            finance.ebitda = int(input("Enter ebitda (in the format '987654321'):\n"))
            finance.sales = int(input("Enter sales (in the format '987654321'):\n"))
            finance.net_profit = int(input("Enter net profit (in the format '987654321'):\n"))
            finance.market_price = int(input("Enter market price (in the format '987654321'):\n"))
            finance.net_debt = int(input("Enter net debt (in the format '987654321'):\n"))
            finance.assets = int(input("Enter assets (in the format '987654321'):\n"))
            finance.equity = int(input("Enter equity (in the format '987654321'):\n"))
            finance.cash_equivalents = int(input("Enter cash equivalents (in the format '987654321'):\n"))
            finance.liabilities = int(input("Enter liabilities (in the format '987654321'):\n"))

            self.session.commit()
            print("Company updated successfully!")
            return State.MAIN_MENU

    def delete_company(self):
        name = input("Enter company name:\n")

        companies = self.session.query(Companies).filter(Companies.name.like(f"%{name}%")).all()
        if not companies:
            print("Company not found!")
            return State.MAIN_MENU
        else:
            for index, company in enumerate(companies):
                print(f"{index} {company.name}")
            chosen_index = int(input("Enter company number:\n"))
            ticker = companies[chosen_index].ticker
            self.session.query(Financial).filter(Financial.ticker == ticker).delete()
            self.session.query(Companies).filter(Companies.ticker == ticker).delete()
            self.session.commit()
            print("Company deleted successfully!")
            return State.MAIN_MENU

    def list_companies(self):
        print("COMPANY LIST")
        companies = self.session.query(Companies).order_by(Companies.ticker).all()
        for company in companies:
            print(f"{company.ticker} {company.name} {company.sector}")
        return State.MAIN_MENU
    
    def list_companies_by_calc(self, state: State):

        financials = self.session.query(Financial).all()

        match state:
            case State.LIST_COMPANIES_BY_ND_EBITDA:
                print("TICKER ND/EBITDA")
                financials = sorted(financials, key=lambda financial: financial.get_NB_EBITDA_num(), reverse=True)
            case State.LIST_COMPANIES_BY_ROE:
                print("TICKER ROE")
                financials = sorted(financials, key=lambda financial: financial.get_ROE_num(), reverse=True)
            case State.LIST_COMPANIES_BY_ROA:
                print("TICKER ROA")
                financials = sorted(financials, key=lambda financial: financial.get_ROA_num(), reverse=True)

        counter = 0
        for financial in financials:
            if counter == 10: break
            match state:
                case State.LIST_COMPANIES_BY_ND_EBITDA:
                    print(f"{financial.ticker} {financial.get_NB_EBITDA()}")
                case State.LIST_COMPANIES_BY_ROE:
                    print(f"{financial.ticker} {financial.get_ROE()}")
                case State.LIST_COMPANIES_BY_ROA:
                    print(f"{financial.ticker} {financial.get_ROA()}")
            counter += 1
        return State.MAIN_MENU








