
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
        # Safely get book details even if book was deleted
        book_title = log.book.title if log.book else "[Deleted Book]"
        
        # Safely get user details even if user was deleted
        user_name = log.user.name if log.user else "[Deleted User]"
        
        borrowed_at_str = log.borrowed_at.strftime("%Y-%m-%d %H:%M") if log.borrowed_at else "N/A"
        returned_at_str = log.returned_at.strftime("%Y-%m-%d %H:%M") if log.returned_at else "Not returned"
        duration = str(log.duration) if log.duration else "Not returned"
        
        table.add_row([
            log.id,
            book_title,
            user_name,
            borrowed_at_str,
            returned_at_str,
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

def delete_user():
    print("\nDelete User")
    view_users()
    user_id = input("Enter user ID to delete: ").strip()
    
    try:
        user_id = int(user_id)
        user = session.get(User, user_id)
        
        if not user:
            print("❌ User not found")
            return
            
        # Check for active borrows
        active_borrows = session.query(BorrowLog).filter(
            BorrowLog.user_id == user_id,
            BorrowLog.returned_at.is_(None)
        ).count()
        
        if active_borrows > 0:
            print(f"❌ User has {active_borrows} active borrows. Cannot delete.")
            return
            
        # Check for any borrow history
        borrow_history = session.query(BorrowLog).filter_by(user_id=user_id).count()
        if borrow_history > 0:
            confirm = input(f"⚠️ User has {borrow_history} borrow records. Delete anyway? (y/n): ").lower()
            if confirm != 'y':
                print("❌ Deletion canceled")
                return
                
        # Set user_id to NULL in borrow logs
        session.query(BorrowLog).filter_by(user_id=user_id).update({BorrowLog.user_id: None})
        session.delete(user)
        session.commit()
        print(f"✅ User '{user.name}' deleted successfully")
    except ValueError:
        print("❌ Invalid user ID")

def delete_author():
    print("\nDelete Author")
    view_authors()
    author_id = input("Enter author ID to delete: ").strip()
    
    try:
        author_id = int(author_id)
        author = session.get(Author, author_id)
        
        if not author:
            print("❌ Author not found")
            return
            
        # Check for borrowed books
        borrowed_books = session.query(Book).filter(
            Book.author_id == author_id,
            Book.currently_borrowed == True
        ).count()
        
        if borrowed_books > 0:
            print(f"❌ Author has {borrowed_books} books currently borrowed. Cannot delete.")
            return
            
        # Check for associated books
        book_count = session.query(Book).filter_by(author_id=author_id).count()
        if book_count > 0:
            confirm = input(f"⚠️ Author has {book_count} books. Delete author and all their books? (y/n): ").lower()
            if confirm != 'y':
                print("❌ Deletion canceled")
                return
                
            # Delete books and their borrow logs
            books = session.query(Book).filter_by(author_id=author_id).all()
            for book in books:
                # Delete borrow logs for book
                session.query(BorrowLog).filter_by(book_id=book.id).delete()
                session.delete(book)
                
        session.delete(author)
        session.commit()
        print(f"✅ Author '{author.name}' deleted successfully")
    except ValueError:
        print("❌ Invalid author ID")

def delete_book():
    print("\nDelete Book")
    view_books()
    book_id = input("Enter book ID to delete: ").strip()
    
    try:
        book_id = int(book_id)
        book = session.get(Book, book_id)
        
        if not book:
            print("❌ Book not found")
            return
            
        if book.currently_borrowed:
            print("❌ Book is currently borrowed. Cannot delete.")
            return
            
        # Check for borrow history
        borrow_count = session.query(BorrowLog).filter_by(book_id=book_id).count()
        if borrow_count > 0:
            confirm = input(f"⚠️ Book has {borrow_count} borrow records. Delete anyway? (y/n): ").lower()
            if confirm != 'y':
                print("❌ Deletion canceled")
                return
                
        # Delete associated borrow logs
        session.query(BorrowLog).filter_by(book_id=book_id).delete()
        session.delete(book)
        session.commit()
        print(f"✅ Book '{book.title}' deleted successfully")
    except ValueError:
        print("❌ Invalid book ID")


def find_user():
    print("\nSearch Users")
    search_term = input("Enter name to search: ").strip()
    if not search_term:
        print("❌ Please enter a search term")
        return
        
    users = session.query(User).filter(User.name.ilike(f"%{search_term}%")).all()
    
    if not users:
        print("❌ No users found")
        return
        
    table = PrettyTable()
    table.field_names = ["ID", "Name", "Age", "Gender", "Active Borrows", "Past Borrows"]
    
    for user in users:
        # Get active borrows (not returned yet)
        active_borrows = session.query(BorrowLog).filter(
            BorrowLog.user_id == user.id,
            BorrowLog.returned_at.is_(None)
        ).count()
        
        # Get past borrows (already returned)
        past_borrows = session.query(BorrowLog).filter(
            BorrowLog.user_id == user.id,
            BorrowLog.returned_at.isnot(None)
        ).count()
        
        table.add_row([
            user.id,
            user.name,
            user.age,
            user.gender,
            active_borrows,
            past_borrows
        ])
    
    print(table)

def find_author():
    print("\nSearch Authors")
    search_term = input("Enter name to search: ").strip()
    if not search_term:
        print("❌ Please enter a search term")
        return
        
    authors = session.query(Author).filter(Author.name.ilike(f"%{search_term}%")).all()
    
    if not authors:
        print("❌ No authors found")
        return
        
    table = PrettyTable()
    table.field_names = ["ID", "Name", "Book Count"]
    for author in authors:
        book_count = session.query(Book).filter_by(author_id=author.id).count()
        table.add_row([author.id, author.name, book_count])
    print(table)

def find_book():
    print("\nSearch Books")
    search_term = input("Enter title, author, or genre: ").strip()
    if not search_term:
        print("❌ Please enter a search term")
        return
        
    books = session.query(Book).join(Author).filter(
        Book.title.ilike(f"%{search_term}%") | 
        Author.name.ilike(f"%{search_term}%") | 
        Book.genre.ilike(f"%{search_term}%")
    ).all()
    
    if not books:
        print("❌ No books found")
        return
        
    table = PrettyTable()
    table.field_names = ["ID", "Title", "Author", "Genre", "Status"]
    for book in books:
        author_name = book.author.name if book.author else "Unknown"
        status = "Borrowed" if book.currently_borrowed else "Available"
        table.add_row([book.id, book.title, author_name, book.genre, status])
    print(table)
