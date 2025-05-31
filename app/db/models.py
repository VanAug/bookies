
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime, timedelta

engine = create_engine("sqlite:///bookies.db")
BASE = declarative_base()

class Author(BASE):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    #one author has multiple books
    books = relationship("Book", back_populates="author")

class Book(BASE):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    genre = Column(String)
    currently_borrowed = Column(Boolean, default=False)
    author_id = Column(Integer, ForeignKey('authors.id'))

    #Relationships
    author = relationship("Author", back_populates="books")
    borrow_logs = relationship("BorrowLog", back_populates="book")

class User(BASE):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)

    #One user has many borrow logs
    borrow_logs = relationship("BorrowLog", back_populates="user")

class BorrowLog(BASE):
    __tablename__ = 'borrow_logs'

    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    borrowed_at = Column(DateTime, default=datetime.now())
    returned_at = Column(DateTime, nullable=True)

    #Relationships
    book = relationship("Book", back_populates="borrow_logs")
    user = relationship("User", back_populates="borrow_logs")

    @property
    def duration(self) -> timedelta:
        if self.returned_at and self.borrowed_at:
            return self.returned_at - self.borrowed_at
        return None