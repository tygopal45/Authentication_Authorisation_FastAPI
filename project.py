from fastapi import FastAPI, Depends
from database import get_db
from sqlalchemy.orm import Session
import model
from pydantic import BaseModel

app = FastAPI()

# Creating API

class Bookstore(BaseModel):
    id: int
    title: str
    author: str
    publish_date: str


@app.post("/books/")
def create_book(book: Bookstore, db: Session = Depends(get_db)):
    db_book = model.Book(id=book.id, title=book.title, author=book.author, publish_date=book.publish_date)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

@app.get("/books/{book_id}")
def read_book(book_id: int, db: Session = Depends(get_db)):
    return db.query(model.Book).filter(model.Book.id == book_id).first()

@app.put("/all_books")
def get_book(book: Bookstore, db: Session = Depends(get_db)):
    db_book = db.query(model.Book).all()
    return db_book