from sqlalchemy.orm import Session
from app.models import Article, Comment
from app.schemas import ArticleCreate, ArticleUpdate

# Article CRUD
def create_article(db: Session, article: ArticleCreate):
    db_article = Article(**article.dict())
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article

def get_article(db: Session, article_id: int):
    return db.query(Article).filter(Article.id == article_id).first()

def get_articles(db: Session, skip: int = 0, limit: int = 10, author: str = None, category: str = None):
    query = db.query(Article)
    if author:
        query = query.filter(Article.author == author)
    if category:
        query = query.filter(Article.category == category)
    return query.offset(skip).limit(limit).all()

def update_article(db: Session, article_id: int, article: ArticleUpdate):
    db_article = get_article(db, article_id)
    if db_article:
        for key, value in article.dict(exclude_unset=True).items():
            setattr(db_article, key, value)
        db.commit()
        db.refresh(db_article)
    return db_article

def delete_article(db: Session, article_id: int):
    db_article = get_article(db, article_id)
    if db_article:
        db.delete(db_article)
        db.commit()
    return db_article

# Comment CRUD
def create_comment(db: Session, article_id: int, content: str):
    comment = Comment(content=content, article_id=article_id)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment
