from pydantic import BaseModel
from typing import List, Optional

class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    pass

class Comment(CommentBase):
    id: int
    article_id: int

    class Config:
        orm_mode = True

class ArticleBase(BaseModel):
    title: str
    content: str
    author: str
    category: str

class ArticleCreate(ArticleBase):
    pass

class ArticleUpdate(BaseModel):
    title: Optional[str]
    content: Optional[str]
    author: Optional[str]
    category: Optional[str]

class Article(ArticleBase):
    id: int
    comments: List[Comment] = []

    class Config:
        orm_mode = True
