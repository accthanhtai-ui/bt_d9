from fastapi import FastAPI, Depends, HTTPException
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
# 4. FASTAPI
# =========================================================

app = FastAPI(
    title="Library Management - Bài 2"
)


# =========================================================
# 5. API DELETE /books/{id}
# =========================================================

@app.delete("/books/{book_id}")
def delete_book(
    book_id: int,
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

    # Xóa sách
    db.delete(db_book)

    # Lưu thay đổi vào MySQL
    db.commit()

    # Trả về thông báo
    return {
        "message": f"Đã xóa thành công sách ID {book_id}"
    }