from pydantic import BaseModel, ConfigDict, Field, EmailStr
# BaseModel -> BaseClass which all Pydantic model inherit from
# Field allows you add constraint like Min and Max
# Modern Pydantic model
# improves validation of data, determines what data goes in what comes out
from datetime import datetime

class UserBase(BaseModel):
    username: str = Field(min_length=1, max_length=50)
    email: EmailStr = Field(max_length=120)
    
class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    pass


class PostBase(BaseModel):
    title: str = Field(min_length = 1, max_length = 100)
    content: str = Field(min_length = 1)
    author: str = Field(min_length = 1, max_length = 50)

class PostCreate(PostBase):         #inheritance
    pass

class PostResponse(PostBase):
    model_config = ConfigDict(from_attributes=True)     #Reads Data from attributes

    id: int
    date_posted: str