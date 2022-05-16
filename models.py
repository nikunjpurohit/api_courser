from pickle import TRUE
from psycopg2 import Timestamp
from databse import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP



class Post (Base):
    __tablename__ = "posts_1"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    title = Column( String, nullable =False)
    content = Column(String, nullable =False)
    published = Column(Boolean, nullable =False, default=True)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False, default=text('now()'))
    

class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True,nullable=False,unique=True )
    email=Column(String,nullable=False,unique=True )
    password=Column(String,nullable=False )
    created_at = Column(TIMESTAMP(timezone=True),nullable=False, default=text('now()'))