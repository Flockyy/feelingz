from typing import List, Optional
from pydantic import BaseModel

class DocumentBase(BaseModel):
    text: str

class DocumentCreate(DocumentBase):
    pass

class Document(DocumentCreate):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

# User Schemas
class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class User(UserCreate):
    id: int
    is_active: bool
    Documents : list[Document] = []
    
    class Config:
        orm_mode = True