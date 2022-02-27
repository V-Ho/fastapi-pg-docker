from pydantic import BaseModel

# Pydantic model used to define schema of API requests and responses
class PostBase(BaseModel):  # Post pydantic class extends BaseModel
    title: str
    content: str
    published: bool = True  # if user doesn't provide published value, use 'True' as default
    #rating: Optional[int] = None # if user doesn't provide value, defaults to None

class PostCreate(PostBase):
    pass