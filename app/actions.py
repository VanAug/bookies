
from sqlalchemy.orm import sessionmaker
from db.models import Author, User, Book, BorrowLog, engine
from prettytable import PrettyTable

session = sessionmaker(bind=engine)()

#Helper function to display books
def _display_books(books):
    table = PrettyTable()
    table.field_names = ["ID", "Title", "Genre", "Author", "Borrowed"]
    for book in books:
        author_name = book.author.name if book.author else "Unknown"
        borrowed = "Yes" if book.currently_borrowed else "No"
        table.add_row([book.id, book.title, book.genre, author_name, borrowed])
    print(table)

def view_books():
    books = session.query(Book).all()
    _display_books(books)

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