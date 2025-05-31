
from sqlalchemy.orm import sessionmaker
from db.models import Author, User, Book, BorrowLog, engine
from prettytable import PrettyTable
from datetime import datetime

session = sessionmaker(bind=engine)()

# Helper function to display books
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
    users = session.query(User).all()
    table = PrettyTable()
    table.field_names = ["ID", "Name", "Age", "Gender"]
    for user in users:
        table.add_row([user.id, user.name, user.age, user.gender])
    print(table)

def view_authors():
    authors = session.query(Author).all()
    table = PrettyTable()
    table.field_names = ["ID", "Name"]
    for author in authors:
        table.add_row([author.id, author.name])
    print(table)

def view_borrow_logs():
    logs = session.query(BorrowLog).all()
    table = PrettyTable()
    table.field_names = ["Log ID", "Book", "User", "Borrowed At", "Returned At", "Duration"]
    
    for log in logs:
        duration = str(log.duration) if log.duration else "Not returned"
        returned_at = log.returned_at.strftime("%Y-%m-%d %H:%M") if log.returned_at else "Not returned"
        table.add_row([
            log.id,
            log.book.title,
            log.user.name,
            log.borrowed_at.strftime("%Y-%m-%d %H:%M"),
            returned_at,
            duration
        ])
    print(table)

def add_book():
    print("\nAdd New Book")
    title = input("Title: ").strip()
    genre = input("Genre (optional): ").strip() or None
    author_name = input("Author: ").strip()
    
    # Find or create author
    author = session.query(Author).filter(Author.name.ilike(author_name)).first()
    if not author:
        author = Author(name=author_name)
        session.add(author)
        session.flush()  # Get ID without committing transaction
    
    book = Book(title=title, genre=genre, author_id=author.id)
    session.add(book)
    session.commit()
    print(f"✅ Book '{title}' added successfully!")

def add_author():
    print("\nAdd New Author")
    name = input("Name: ").strip()
    author = Author(name=name)
    session.add(author)
    session.commit()
    print(f"✅ Author '{name}' added successfully!")

def add_user():
    print("\nAdd New User")
    name = input("Name: ").strip()
    age = int(input("Age: "))
    gender = input("Gender: ").strip()
    
    user = User(name=name, age=age, gender=gender)
    session.add(user)
    session.commit()
    print(f"✅ User '{name}' added successfully!")

def mark_as_borrowed():
    print("\nMark Book as Borrowed")
    view_books()
    book_id = int(input("Enter book ID: "))
    view_users()
    user_id = int(input("Enter user ID: "))
    
    book = session.get(Book, book_id)
    user = session.get(User, user_id)
    
    if not book or not user:
        print("❌ Invalid book or user ID")
        return
    
    if book.currently_borrowed:
        print("❌ Book is already borrowed")
        return
    
    # Create borrow log
    borrow_log = BorrowLog(book_id=book_id, user_id=user_id)
    book.currently_borrowed = True
    session.add(borrow_log)
    session.commit()
    print(f"✅ '{book.title}' marked as borrowed by {user.name}")

def mark_as_returned():
    print("\nMark Book as Returned")
    # Show active borrows
    active_borrows = session.query(BorrowLog).filter_by(returned_at=None).all()
    
    if not active_borrows:
        print("❌ No active borrows found")
        return
    
    table = PrettyTable()
    table.field_names = ["Log ID", "Book", "User", "Borrowed At"]
    for log in active_borrows:
        table.add_row([
            log.id,
            log.book.title,
            log.user.name,
            log.borrowed_at.strftime("%Y-%m-%d %H:%M")
        ])
    print(table)
    
    log_id = int(input("Enter borrow log ID: "))
    borrow_log = session.get(BorrowLog, log_id)
    
    if not borrow_log or borrow_log.returned_at:
        print("❌ Invalid or already returned log")
        return
    
    borrow_log.returned_at = datetime.now()
    borrow_log.book.currently_borrowed = False
    session.commit()
    print(f"✅ '{borrow_log.book.title}' marked as returned")

def get_available_books():
    books = session.query(Book).filter_by(currently_borrowed=False).all()
    print("\nAvailable Books:")
    _display_books(books)

def get_borrowed_books():
    books = session.query(Book).filter_by(currently_borrowed=True).all()
    print("\nBorrowed Books:")
    _display_books(books)