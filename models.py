from sqlalchemy import Boolean, Column, ForeignKey, Integer, String ,DateTime,FLOAT
from sqlalchemy.orm import relationship
import datetime
from database import Base


class Trade(Base):
    __tablename__ = "trade"

    trade_id = Column(String, primary_key=True, index=True)

    trader = Column(String)

    asset_class = Column(String)
    
    counterparty= Column(String)

    instrument_id = Column(String)

    instrument_name = Column(String)

    trade_date_time = DateTime()

    trade_details = Column(String)

class TradeDetails(Base):
    __tablename__ = "tradedetails"
    
    trade_id = Column(String, primary_key=True, index=True)

    buySellIndicator = Column(String)

    price = Column(FLOAT)

    quantity = Column(Integer)

