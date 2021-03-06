import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

# Restaurant class
class Restaurant(Base):
    # Tables
    __tablename__ = 'restaurant'

    # Mapper
    id = Column(Integer,primary_key=True)
    name = Column(String(250),nullable=False)
    city = Column(String(250),nullable=False)


class MenuItem(Base):
    # Tables
    __tablename__ = 'menu_item'

    # Mapper
    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    price = Column(String(8))
    course = Column(String(250))
    restaurant_id = Column(Integer, ForeignKey('restaurant.id')) # Column( Integer, ForeignKey('<tablename.foreignkeyfield>'))
    restaurant = relationship(Restaurant) # relationship(<className>)

    @property
    def serialize(self):
        return {
                'name':self.name,
                'description':self.description,
                'id':self.id,
                'price':self.price,
                'course':self.course
                }

engine = create_engine('sqlite:///app.db')


Base.metadata.create_all(engine)