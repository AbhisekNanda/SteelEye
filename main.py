from fastapi import FastAPI,Depends
from sqlalchemy.orm import Session
from sqlalchemy import and_
from database import SessionLocal,engine
import models
from fastapi.encoders import jsonable_encoder
import schemas
from pydantic import BaseModel
import datetime
models.Base.metadata.create_all(bind=engine)

app=FastAPI() 

#Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally :
        db.close()

@app.get("/all")
def index(db:Session = Depends(get_db)):
    all_treades=db.query(models.Trade).all()
    return jsonable_encoder(all_treades)


@app.get("/trade")
def trade(id ,db:Session = Depends(get_db)):
    trade=db .query(models.Trade).filter(models.Trade.trade_id == id).first()
    return jsonable_encoder(trade)

class search(BaseModel):
    search :str

@app.post('/search')
def search(search:search,db:Session = Depends(get_db)):
    x=db.query(models.Trade).all()
    search_trade = db.query(models.Trade).filter( models.Trade.counterparty.like('%'+search.search+'%') | models.Trade.instrument_id.like('%'+search.search+'%') | models.Trade.instrument_name.like('%'+search.search+'%') | models.Trade.trader.like('%'+search.search+'%')).all()
    #courses.filter(models.Course.name.like('%' + searchForm.courseName.data + '%'))
    return jsonable_encoder(search_trade)

class filter(BaseModel):
    assetClass : str
    end : str
    maxPrice :str
    minPrice :str
    start : str
    tradeType : str

@app.post('/filter')
def filter(filter:filter , db:Session = Depends(get_db)):
    
    x=db.query(models.Trade,models.TradeDetails).filter(models.Trade.trade_id == models.TradeDetails.trade_id)
    if filter.assetClass :
        x=x.filter(models.Trade.asset_class == filter.assetClass)
    if filter.end:
        x=x.filter(models.Trade.trade_date_time == filter.end)
    if filter.maxPrice:
        x=x.filter(models.TradeDetails.price <= filter.maxPrice)
    if filter.minPrice :
        x=x.filter(models.TradeDetails.price >= filter.minPrice)
    if filter.tradeType :
        x=x.filter(models.TradeDetails.buySellIndicator == filter.tradeType)
    
    data = x.all()

    return jsonable_encoder(data)


