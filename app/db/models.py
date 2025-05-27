
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base
from datetime import datetime

engine = create_engine("sqlite:///bookies.db")
BASE = declarative_base()

class Author(BASE):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

class Book(BASE):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    genre = Column(String)
    is_read = Column(Boolean, default=False)
    author_id = Column(Integer, ForeignKey('authors.id'))

class User(BASE):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

class BorrowLog(BASE):
    __tablename__ = 'borrow_logs'

    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    borrowed_at = Column(DateTime, default=datetime.now())
    returned_at = Column(DateTime, nullable=True)