# server/seed.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Author, Book, Review

# 1. Connect to the database
engine = create_engine('sqlite:///litlog.db')
Session = sessionmaker(bind=engine)
session = Session()

def seed_data():
    print("🌱 Clearing old data...")
    # Delete existing data to start fresh every time we run this script
    session.query(Review).delete()
    session.query(Book).delete()
    session.query(Author).delete()

    print("🌱 Creating Authors...")
    author1 = Author(name="J.K. Rowling", bio="British author, philanthropist, and film producer.")
    author2 = Author(name="George Orwell", bio="English novelist and essayist, journalist and critic.")
    author3 = Author(name="J.R.R. Tolkien", bio="English writer, poet, philologist, and academic.")

    session.add_all([author1, author2, author3])
    session.commit() # We commit here to generate IDs for the authors

    print("🌱 Creating Books...")
    book1 = Book(title="Harry Potter and the Sorcerer's Stone", genre="Fantasy", publish_date="1997", author_id=author1.id)
    book2 = Book(title="1984", genre="Dystopian", publish_date="1949", author_id=author2.id)
    book3 = Book(title="The Hobbit", genre="Fantasy", publish_date="1937", author_id=author3.id)
    book4 = Book(title="Animal Farm", genre="Satire", publish_date="1945", author_id=author2.id)

    session.add_all([book1, book2, book3, book4])
    session.commit()

    print("🌱 Creating Reviews...")
    review1 = Review(rating=5, content="Absolutely magical! Defined my childhood.", book_id=book1.id)
    review2 = Review(rating=4, content="Scary but important read.", book_id=book2.id)
    review3 = Review(rating=5, content="A classic adventure.", book_id=book3.id)

    session.add_all([review1, review2, review3])
    session.commit()

    print("✅ Done! Database populated.")

if __name__ == '__main__':
    seed_data()