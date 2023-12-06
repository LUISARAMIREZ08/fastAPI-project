from pydantic import BaseModel, Field
from typing import Optional
import time


class Movie(BaseModel):
    id: Optional[int] = None
    title:str = Field(min_length=2,max_length=40)
    overview:str = Field(min_length=20,max_length=300)
    year:int = Field(le=time.localtime().tm_year)
    rating:float = Field(ge= 0, le=10)
    category:str = Field(min_length=5,max_length=12)
