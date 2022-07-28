from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.models import store
from app.schemas import schemas

# from . import models, schemas
from app.api.dependb import get_db

# from .config import settings

router = APIRouter()


@router.get(
    "/books", response_model=list[schemas.Book], status_code=status.HTTP_200_OK
)
def get_all_books(
    db: Session = Depends(get_db), skip: int = 0, limit: int = 100
):
    books = db.query(store.Book).offset(skip).limit(limit).all()
    return books


@router.post(
    "/books", response_model=schemas.Book, status_code=status.HTTP_201_CREATED
)
def create_book(book: schemas.CreatedBook, db: Session = Depends(get_db)):
    db_item = db.query(store.Book).filter(store.Book.name == book.name).first()
    if db_item is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Book with name:'{book.name}' already exists",
        )

    new_book = store.Book(
        name=book.name,
        price=book.price,
        description=book.description,
        is_active=book.is_active,
    )

    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


@router.get(
    "/books/{book_id}",
    response_model=schemas.Book,
    status_code=status.HTTP_200_OK,
)
def get_book_by_id(book_id: int, db: Session = Depends(get_db)):
    book = db.query(store.Book).filter(store.Book.id == book_id).first()

    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {book_id} not found",
        )

    return book


@router.put(
    "/books/{book_id}",
    response_model=schemas.Book,
    status_code=status.HTTP_200_OK,
)
def update_book_by_id(
    book_id: int, book: schemas.Book, db: Session = Depends(get_db)
):
    book_to_update = (
        db.query(store.Book).filter(store.Book.id == book_id).first()
    )

    if not book_to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {book_id} not found",
        )

    book_to_update.name = book.name
    book_to_update.price = book.price
    book_to_update.description = book.description
    book_to_update.is_active = book.is_active

    db.commit()
    db.refresh(book_to_update)

    return book_to_update


# mb use status code 204, but it doesn't return deleted object
@router.delete("/books/{book_id}", status_code=status.HTTP_200_OK)
def delete_book_by_id(book_id: int, db: Session = Depends(get_db)):
    book_to_delete = (
        db.query(store.Book).filter(store.Book.id == book_id).first()
    )

    if not book_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {book_id} not found",
        )

    db.delete(book_to_delete)
    db.commit()

    return {"detail": "Book deleted successfully", "Book": book_to_delete}
