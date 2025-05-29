
from sqlalchemy.orm import sessionmaker
from db.models import Author, User, Book, BorrowLog, engine
from prettytable import PrettyTable

session = sessionmaker(bind=engine)()

def view_books():
    print("Books")

def view_users():
    print("users")

def view_authors():
    print("authors")

def view_borrow_logs():
    print("logs")

def add_book():
    print("add books")

def add_author():
    print("add author")

def add_user():
    print("add user")

def add_borrow_log():
    print("add log")

def mark_as_borrowed():
    print("mark borrowed")

def mark_as_returned():
    print("mark returned")

def get_available_books():
    print("available books")

def get_borrowed_books():
    print("borrowed books")