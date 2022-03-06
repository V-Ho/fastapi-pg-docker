from datetime import datetime
from pydantic import BaseModel, EmailStr

# Pydantic model used to define schema of API requests and responses
class PostBase(BaseModel):  # Post pydantic class extends BaseModel
    title: str
    content: str
    published: bool = True  # if user doesn't provide published value, use 'True' as default
    #rating: Optional[int] = None # if user doesn't provide value, defaults to None

class PostCreate(PostBase):
    pass

# how we send data to user in response
class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    # created_at: datetime

class UserOut(BaseModel):
    id: int
    email: EmailStr
    # created_at: datetime

    class Config:
        orm_mode = True
