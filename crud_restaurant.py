from sqlalchemy import create_engine
from database_setup import Base, Restaurant,MenuItem
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///app.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

def createRestaurant(restaurant):
    if type(restaurant) is Restaurant:
        session.add(restaurant)
        session.commit(restaurant)
def readAllRestaurant():
    restaurants = session.query(Restaurant).all()
    return restaurants
def deleteRestaurant(rest_id):
    try:
        restaurant = session.query(Restaurant).filter_by(id=rest_id).one()
        menus = session.query(MenuItem).filter_by(restaurant_id = rest_id).one()
        session.delete(restaurant)
        for i in menus:
            session.delete(i)
        session.commit()
        return True
    except Exception:
        return False