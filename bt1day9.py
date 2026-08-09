from typing import Optional

from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, declarative_base, Session


# =========================================================
# 1. KẾT NỐI MYSQL
# =========================================================

DATABASE_URL = "mysql+pymysql://root:jay2007@localhost:3306/library_management"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


# =========================================================
# 2. MODEL BOOK
# =========================================================

class Book(Base):
    __tablename__ = "books"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    title = Column(
        String(255),
        nullable=False
    )

    author = Column(
        String(100),
        nullable=False
    )

    price = Column(
        Float,
        nullable=False
    )

    quantity = Column(
        Integer,
        default=0
    )


# =========================================================
# 3. DATABASE DEPENDENCY
# =========================================================

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# =========================================================
# 4. PYDANTIC SCHEMA
# =========================================================

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None


# =========================================================
# 5. FASTAPI
# =========================================================

app = FastAPI(
    title="Library Management - Bài 1"
)


# =========================================================
# 6. API PUT /books/{id}
# =========================================================

@app.put("/books/{book_id}")
def update_book(
    book_id: int,
    book_in: BookUpdate,
    db: Session = Depends(get_db)
):

    # Tìm sách trong database
    db_book = (
        db.query(Book)
        .filter(Book.id == book_id)
        .first()
    )

    # Nếu không tìm thấy
    if db_book is None:
        raise HTTPException(
            status_code=404,
            detail="Sách không tồn tại trong hệ thống"
        )

    # Lấy những trường được gửi lên
    update_data = book_in.model_dump(
        exclude_unset=True
    )

    # Cập nhật từng trường
    for field, value in update_data.items():
        setattr(db_book, field, value)

    # Lưu vào MySQL
    db.commit()

    # Refresh dữ liệu
    db.refresh(db_book)

    # Trả về sách sau khi cập nhật
    return db_book