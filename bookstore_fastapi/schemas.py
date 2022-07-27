from pydantic import BaseModel


class Book(BaseModel):
    id: int
    name: str
    price: float
    description: str
    is_active: bool = True
    #author_id: int
    #category_id: int

    class Config:
        orm_mode=True
    