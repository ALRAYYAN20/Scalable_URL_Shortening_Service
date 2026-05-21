from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy import func
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'user'

    id = mapped_column(Integer, primary_key = True)
    # int column created and primary key = True means, ids will auto increament from 1
    username : Mapped[str] = mapped_column(String(50))
    # creates column just like above , this syntax is shortcut, CANNOT BE NULL
    email : Mapped[str] = mapped_column(String (100), unique = True, nullable = False)
    # same, cannot be null
    password : Mapped[str] = mapped_column(String (255))
    # stores password 
    create_date : Mapped[datetime] = mapped_column(insert_default = func.now())
    # notes time when data was created
    urls = relationship('URL', back_populates='owner')

 

class URL(Base):
    __tablename__ = 'url'

    owner_id = mapped_column ( ForeignKey('user.id'))
    id = mapped_column ( Integer, primary_key = True)
    original_url: Mapped[str] = mapped_column ( nullable = False )
    short_code : Mapped[str] = mapped_column ( String(10), unique = True, nullable = False )
    click_count : Mapped[int] = mapped_column ( default = 0 )
    created_at: Mapped[datetime] = mapped_column ( insert_default = func.now() )
    expires_at: Mapped[datetime] = mapped_column( nullable = False)
    owner = relationship( 'User', back_populates='urls' )

