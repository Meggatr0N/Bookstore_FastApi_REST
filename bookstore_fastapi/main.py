from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from . import actions, models, schemas
from .db import SessionLocal, engine
from . import models

# Create all tables in the database.
# Comment this out if you using migrations.
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get DB session.
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get("/")
def index():
    return {"message": "Hello world!"}



@app.get('/books', response_model=list[schemas.Book], status_code=status.HTTP_200_OK)
def get_all_books(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    books = db.query(models.Book).offset(skip).limit(limit).all()
    return books


@app.post('/books', response_model=schemas.Book, status_code=status.HTTP_201_CREATED)
def create_book(book: schemas.Book, db: Session = Depends(get_db)):
    db_item = db.query(models.Book).filter(models.Book.name == book.name).first()
    if db_item is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Book already exists')


    new_book = models.Book(
        name=book.name,
        price=book.price,
        description=book.description,
        is_active=book.is_active
    )

    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


@app.get('/books/{book_id}', response_model=schemas.Book, status_code=status.HTTP_200_OK)
def get_book_by_id(book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()

    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book is not found")

    return book


@app.put('/books/{book_id}', response_model=schemas.Book, status_code=status.HTTP_200_OK)
def update_book_by_id(book_id: int, book: schemas.Book, db: Session = Depends(get_db)):
    book_to_update = db.query(models.Book).filter(models.Book.id == book_id).first()

    if not book_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book is not found")

    book_to_update.name = book.name
    book_to_update.price = book.price
    book_to_update.description = book.description
    book_to_update.is_active = book.is_active

    db.commit()
    db.refresh(book_to_update)

    return book_to_update


@app.delete('/books/{book_id}')
def delete_book_by_id(book_id: int, db: Session = Depends(get_db)):
    book_to_delete = db.query(models.Book).filter(models.Book.id == book_id).first()

    if not book_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Book is not found')

    db.delete(book_to_delete)
    db.commit()

    return book_to_delete



#poetry shell
#uvicorn bookstore_fastapi.main:app --reload