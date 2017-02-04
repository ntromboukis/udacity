from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

# sets up a user table
class User(Base):
    __tablename__ = 'user'

    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    picture = Column(String(80))
    email = Column(String(250), nullable=False)

# sets up a store table
class Store(Base):
    __tablename__ = 'store'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    photo = Column(String(10))
    category = Column(String(20))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'name'         : self.name,
           'id'           : self.id,
           'photo'        : self.photo,
           'category'     : self.category
       }

# sets up a catalog_item table
class CatalogItem(Base):
    __tablename__ = 'catalog_item'

    name =Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    description = Column(String(250))
    price = Column(String(8))
    store_id = Column(Integer,ForeignKey('store.id'))
    store = relationship(Store)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'name'         : self.name,
           'description'  : self.description,
           'id'           : self.id,
           'price'        : self.price,
       }



engine = create_engine('sqlite:///itemcatalog.db')


Base.metadata.create_all(engine)
