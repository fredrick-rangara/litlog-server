# server/main.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from pydantic import BaseModel
from typing import List, Optional

# Import your actual database models
from models import Base, Author, Book, Review

# 1. Database Setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./litlog.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()

# 2. CORS Setup (Allows your Frontend to talk to this Backend)
origins = [
    "http://localhost:3000",  # React usually runs here
    "http://localhost:5173",  # Vite usually runs here
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- PYDANTIC SCHEMAS (Data shapes for sending/receiving JSON) ---
# We need these so FastAPI knows how to convert SQLAlchemy objects to JSON

class AuthorSchema(BaseModel):
    id: int
    name: str
    bio: Optional[str] = None

    class Config:
        from_attributes = True

class BookSchema(BaseModel):
    id: int
    title: str
    genre: Optional[str] = None
    publish_date: Optional[str] = None
    author_id: int

    class Config:
        from_attributes = True

class ReviewSchema(BaseModel):
    id: int
    rating: int
    content: str
    book_id: int

    class Config:
        from_attributes = True

# --- ROUTES (The API Endpoints) ---

@app.get("/")
def read_root():
    return {"message": "Welcome to the LitLog API"}

# 1. AUTHORS
@app.get("/authors", response_model=List[AuthorSchema])
def get_authors(db: Session = Depends(get_db)):
    return db.query(Author).all()

@app.post("/authors", response_model=AuthorSchema)
def create_author(author: AuthorSchema, db: Session = Depends(get_db)):
    # Note: In a real app, we'd remove 'id' from the input schema
    new_author = Author(name=author.name, bio=author.bio)
    db.add(new_author)
    db.commit()
    db.refresh(new_author)
    return new_author

# 2. BOOKS
@app.get("/books", response_model=List[BookSchema])
def get_books(db: Session = Depends(get_db)):
    return db.query(Book).all()

@app.post("/books", response_model=BookSchema)
def create_book(book: BookSchema, db: Session = Depends(get_db)):
    new_book = Book(
        title=book.title, 
        genre=book.genre, 
        publish_date=book.publish_date, 
        author_id=book.author_id
    )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

# 3. REVIEWS
@app.get("/reviews", response_model=List[ReviewSchema])
def get_reviews(db: Session = Depends(get_db)):
    return db.query(Review).all()

@app.post("/reviews", response_model=ReviewSchema)
def create_review(review: ReviewSchema, db: Session = Depends(get_db)):
    new_review = Review(
        rating=review.rating, 
        content=review.content, 
        book_id=review.book_id
    )
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review