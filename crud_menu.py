from sqlalchemy import create_engine
from database_setup import Base, Restaurant,MenuItem
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///app.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

def showAllMenu(restaurant_id):
    menus = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return menus