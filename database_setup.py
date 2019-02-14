# make configuration and that means import all module that will be used
import os
import sys
import sqlalchemy
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

# create object from create_engine to tell sqlalchemy that i use special
# sqlalchemy classes
# that will respond to tables in our database
base = declarative_base()


class User(base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))


class Catalog(base):
        __tablename__ = 'catalog'
        id = Column(Integer, primary_key=True)
        name = Column(String, nullable=False)
        user_id = Column(Integer, ForeignKey('user.id'))
        user = relationship(User)

        @property
        def serialize(self):
            return {
                   'id': self.id,
                   'name': self.name}


class CatalogItem(base):
        __tablename__ = 'item'
        id = Column(Integer, primary_key=True)
        title = Column(String(30), nullable=False)
        description = Column(String(250))
        catalog_id = Column(Integer, ForeignKey('catalog.id'))
        catalog = relationship(Catalog)
        category = Column(String(30), nullable=False)
        user_id = Column(Integer, ForeignKey('user.id'))
        user = relationship(User)
# We added this serialize function to be able to send
# JSON objects in a serializable format

        @property
        def serialize(self):
            return {
                 'id': self.id,

                 'title':  self.title,

                 'description': self.description,

                 'category': self.category,

                 'catalog_id': self.catalog_id}
# to connect with database
engine = create_engine("sqlite:///catalogitem.db")

# add to database the classes that i create as new tables
base.metadata.create_all(engine)
