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
    Book(title="Down and Out in Paris and London", genre="Memoir", currently_borrowed=False, author_id=1),
    Book(title="Homage to Catalonia", genre="History", currently_borrowed=True, author_id=1),
    Book(title="Harry Potter 3", genre="Fantasy", currently_borrowed=False, author_id=2),
    Book(title="Harry Potter 4", genre="Fantasy", currently_borrowed=True, author_id=2),
    Book(title="Emma", genre="Romance", currently_borrowed=False, author_id=3),
    Book(title="Sense and Sensibility", genre="Romance", currently_borrowed=True, author_id=3),
    Book(title="The Adventures of Tom Sawyer", genre="Adventure", currently_borrowed=False, author_id=4),
    Book(title="The Prince and the Pauper", genre="Adventure", currently_borrowed=True, author_id=4),
    Book(title="And Then There Were None", genre="Mystery", currently_borrowed=False, author_id=5),
    Book(title="The Mysterious Affair at Styles", genre="Mystery", currently_borrowed=True, author_id=5),
    Book(title="Anna Karenina", genre="Historical", currently_borrowed=False, author_id=6),
    Book(title="The Death of Ivan Ilyich", genre="Philosophical", currently_borrowed=True, author_id=6),
    Book(title="A Farewell to Arms", genre="Drama", currently_borrowed=False, author_id=7),
    Book(title="For Whom the Bell Tolls", genre="War", currently_borrowed=True, author_id=7),
    Book(title="No Longer at Ease", genre="Tragedy", currently_borrowed=False, author_id=10),
    Book(title="Arrow of God", genre="Historical Fiction", currently_borrowed=True, author_id=10),
    Book(title="Kafka on the Shore", genre="Magical Realism", currently_borrowed=False, author_id=8),
    Book(title="Norwegian Wood", genre="Drama", currently_borrowed=True, author_id=8),
    Book(title="Frankenstein", genre="Gothic", currently_borrowed=False, author_id=9),
    Book(title="The Last Man", genre="Science Fiction", currently_borrowed=True, author_id=9),
]

# Create Users
users = [
    User(name="Alice Johnson", age=28, gender="Female"),
    User(name="Bob Smith", age=32, gender="Male"),
    User(name="Charlie Brown", age=24, gender="Male"),
    User(name="Diana Prince", age=35, gender="Female"),
    User(name="Ethan Hunt", age=40, gender="Male"),
    User(name="Fiona Gallagher", age=29, gender="Female"),
    User(name="George Weasley", age=30, gender="Male"),
    User(name="Hermione Granger", age=27, gender="Female"),
    User(name="Ian Malcolm", age=45, gender="Male"),
    User(name="Jane Foster", age=33, gender="Female"),
]

# Timezone
eat = pytz.timezone("Africa/Nairobi")

# Create BorrowLogs with hardcoded random times
borrow_logs = [
    BorrowLog(book_id=1, user_id=1, borrowed_at=eat.localize(datetime(2024, 4, 1, 10, 0))),
    BorrowLog(book_id=2, user_id=2, borrowed_at=eat.localize(datetime(2024, 3, 15, 9, 30)), 
               returned_at=eat.localize(datetime(2024, 3, 30, 11, 0))),
    BorrowLog(book_id=3, user_id=3, borrowed_at=eat.localize(datetime(2024, 3, 1, 14, 0)), 
               returned_at=eat.localize(datetime(2024, 3, 10, 16, 0))),
    BorrowLog(book_id=4, user_id=4, borrowed_at=eat.localize(datetime(2024, 4, 15, 12, 45))),
    BorrowLog(book_id=5, user_id=5, borrowed_at=eat.localize(datetime(2024, 2, 20, 8, 0)), 
               returned_at=eat.localize(datetime(2024, 3, 5, 9, 0))),
    BorrowLog(book_id=6, user_id=6, borrowed_at=eat.localize(datetime(2024, 4, 10, 10, 15))),
    BorrowLog(book_id=7, user_id=7, borrowed_at=eat.localize(datetime(2024, 1, 25, 11, 0)), 
               returned_at=eat.localize(datetime(2024, 2, 1, 10, 0))),
    BorrowLog(book_id=8, user_id=8, borrowed_at=eat.localize(datetime(2024, 3, 5, 15, 30))),
    BorrowLog(book_id=9, user_id=9, borrowed_at=eat.localize(datetime(2024, 2, 14, 9, 45)), 
               returned_at=eat.localize(datetime(2024, 2, 20, 13, 0))),
    BorrowLog(book_id=10, user_id=10, borrowed_at=eat.localize(datetime(2024, 4, 20, 16, 30))),
    BorrowLog(book_id=12, user_id=1, borrowed_at=eat.localize(datetime(2024, 4, 5, 11, 20))),
    BorrowLog(book_id=14, user_id=3, borrowed_at=eat.localize(datetime(2024, 4, 12, 14, 15))),
    BorrowLog(book_id=16, user_id=5, borrowed_at=eat.localize(datetime(2024, 4, 3, 9, 30))),
    BorrowLog(book_id=18, user_id=7, borrowed_at=eat.localize(datetime(2024, 4, 8, 10, 45))),
    BorrowLog(book_id=20, user_id=9, borrowed_at=eat.localize(datetime(2024, 4, 18, 13, 20))),
    BorrowLog(book_id=22, user_id=2, borrowed_at=eat.localize(datetime(2024, 4, 7, 15, 10))),
    BorrowLog(book_id=24, user_id=4, borrowed_at=eat.localize(datetime(2024, 4, 14, 16, 30))),
    BorrowLog(book_id=26, user_id=6, borrowed_at=eat.localize(datetime(2024, 4, 9, 11, 45))),
    BorrowLog(book_id=28, user_id=8, borrowed_at=eat.localize(datetime(2024, 4, 6, 12, 15))),
    BorrowLog(book_id=30, user_id=10, borrowed_at=eat.localize(datetime(2024, 4, 16, 14, 0))),
]

# Add and commit
session.add_all(authors + books + users + borrow_logs)
session.commit()

print("Dummy data inserted.")
session.close()
