from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.crud import create_article, get_article, get_articles, update_article, delete_article, create_comment
from app.schemas import ArticleCreate, ArticleUpdate, CommentCreate, Article, Comment  # Use Pydantic schemas
from app.database import get_db

router = APIRouter()

@router.post("/articles/", response_model=Article)
def create_new_article(article: ArticleCreate, db: Session = Depends(get_db)):
    return create_article(db, article)

@router.get("/articles/{article_id}", response_model=Article)
def read_article(article_id: int, db: Session = Depends(get_db)):
    db_article = get_article(db, article_id)
    if not db_article:
        raise HTTPException(status_code=404, detail="Article not found")
    return db_article

@router.get("/articles/", response_model=List[Article])
def list_articles(skip: int = 0, limit: int = 10, author: str = None, category: str = None, db: Session = Depends(get_db)):
    return get_articles(db, skip=skip, limit=limit, author=author, category=category)

@router.put("/articles/{article_id}", response_model=Article)
def update_existing_article(article_id: int, article: ArticleUpdate, db: Session = Depends(get_db)):
    return update_article(db, article_id, article)

@router.delete("/articles/{article_id}")
def remove_article(article_id: int, db: Session = Depends(get_db)):
    return delete_article(db, article_id)

@router.post("/articles/{article_id}/comments/", response_model=Comment)
def create_article_comment(article_id: int, comment: CommentCreate, db: Session = Depends(get_db)):
    return create_comment(db, article_id, comment.content)
