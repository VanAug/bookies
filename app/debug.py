from sqlalchemy.orm import sessionmaker
from datetime import datetime, timezone
import pytz

from db.models import BASE, Author, Book, User, BorrowLog
from db.models import engine  # assumes `engine` is also defined in models.py for now


# Set up the session
Session = sessionmaker(bind=engine)
session = Session()

# Clear existing data to avoid duplicates
session.query(BorrowLog).delete()
session.query(Book).delete()
session.query(Author).delete()
session.query(User).delete()
session.commit()

# Create Authors
author1 = Author(name="George Orwell")
author2 = Author(name="J.K. Rowling")

# Create Books
book1 = Book(title="1984", genre="Dystopian", is_read=True, author_id=1)
book2 = Book(title="Animal Farm", genre="Political Satire", is_read=False, author_id=1)
book3 = Book(title="Harry Potter and the Philosopher's Stone", genre="Fantasy", author_id=2)

# Create Users
user1 = User(name="Alice")
user2 = User(name="Bob")

eat = pytz.timezone("Africa/Nairobi")
# Create BorrowLogs
borrow1 = BorrowLog(book_id=1, user_id=1, borrowed_at=datetime.now(eat))
borrow2 = BorrowLog(book_id=3, user_id=2, borrowed_at=datetime.now(eat), returned_at=datetime.now(eat))


# Add and commit
session.add_all([author1, author2, book1, book2, book3, user1, user2, borrow1, borrow2])
session.commit()

print("Dummy data inserted.")
session.close()
