from sqlalchemy.orm import sessionmaker
from datetime import datetime
import pytz

from db.models import BASE, Author, Book, User, BorrowLog, engine

# Setup
BASE.metadata.drop_all(bind=engine)
BASE.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

# Clear existing data
session.query(BorrowLog).delete()
session.query(Book).delete()
session.query(Author).delete()
session.query(User).delete()
session.commit()

# Create Authors
authors = [
    Author(name="George Orwell"),
    Author(name="J.K. Rowling"),
    Author(name="Jane Austen"),
    Author(name="Mark Twain"),
    Author(name="Agatha Christie"),
    Author(name="Leo Tolstoy"),
    Author(name="Ernest Hemingway"),
    Author(name="F. Scott Fitzgerald"),
    Author(name="Haruki Murakami"),
    Author(name="Chinua Achebe")
]

# Create Books
books = [
    Book(title="1984", genre="Dystopian", currently_borrowed=True, author_id=1),
    Book(title="Animal Farm", genre="Political Satire", currently_borrowed=False, author_id=1),
    Book(title="Harry Potter 1", genre="Fantasy", currently_borrowed=False, author_id=2),
    Book(title="Harry Potter 2", genre="Fantasy", currently_borrowed=True, author_id=2),
    Book(title="Pride and Prejudice", genre="Romance", currently_borrowed=False, author_id=3),
    Book(title="Huckleberry Finn", genre="Adventure", currently_borrowed=True, author_id=4),
    Book(title="Murder on the Orient Express", genre="Mystery", currently_borrowed=False, author_id=5),
    Book(title="War and Peace", genre="Historical", currently_borrowed=True, author_id=6),
    Book(title="The Old Man and the Sea", genre="Drama", currently_borrowed=False, author_id=7),
    Book(title="Things Fall Apart", genre="Tragedy", currently_borrowed=True, author_id=10),
]

# Create Users
users = [
    User(name="Alice", age=25, gender="Female"),
    User(name="Bob", age=34, gender="Male"),
    User(name="Charlie", age=28, gender="Male"),
    User(name="Diana", age=22, gender="Female"),
    User(name="Ethan", age=30, gender="Male"),
    User(name="Fiona", age=29, gender="Female"),
    User(name="George", age=31, gender="Male"),
    User(name="Hannah", age=27, gender="Female"),
    User(name="Ian", age=35, gender="Male"),
    User(name="Jane", age=26, gender="Female")
]

# Timezone
eat = pytz.timezone("Africa/Nairobi")

# Create BorrowLogs with hardcoded random times
borrow_logs = [
    BorrowLog(book_id=1, user_id=1, borrowed_at=eat.localize(datetime(2024, 4, 1, 10, 0))),
    BorrowLog(book_id=2, user_id=2, borrowed_at=eat.localize(datetime(2024, 3, 15, 9, 30)), returned_at=eat.localize(datetime(2024, 3, 30, 11, 0))),
    BorrowLog(book_id=3, user_id=3, borrowed_at=eat.localize(datetime(2024, 3, 1, 14, 0)), returned_at=eat.localize(datetime(2024, 3, 10, 16, 0))),
    BorrowLog(book_id=4, user_id=4, borrowed_at=eat.localize(datetime(2024, 4, 15, 12, 45))),
    BorrowLog(book_id=5, user_id=5, borrowed_at=eat.localize(datetime(2024, 2, 20, 8, 0)), returned_at=eat.localize(datetime(2024, 3, 5, 9, 0))),
    BorrowLog(book_id=6, user_id=6, borrowed_at=eat.localize(datetime(2024, 4, 10, 10, 15))),
    BorrowLog(book_id=7, user_id=7, borrowed_at=eat.localize(datetime(2024, 1, 25, 11, 0)), returned_at=eat.localize(datetime(2024, 2, 1, 10, 0))),
    BorrowLog(book_id=8, user_id=8, borrowed_at=eat.localize(datetime(2024, 3, 5, 15, 30))),
    BorrowLog(book_id=9, user_id=9, borrowed_at=eat.localize(datetime(2024, 2, 14, 9, 45)), returned_at=eat.localize(datetime(2024, 2, 20, 13, 0))),
    BorrowLog(book_id=10, user_id=10, borrowed_at=eat.localize(datetime(2024, 4, 20, 16, 30)))
]

# Add and commit
session.add_all(authors + books + users + borrow_logs)
session.commit()

print("Dummy data inserted.")
session.close()
