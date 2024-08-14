from typing import List
from datetime import datetime

from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String, Integer, DateTime, func
from sqlalchemy.orm import sessionmaker, declarative_base, Session

sqlite_url = 'sqlite:///python.db'
engine = create_engine(sqlite_url,
                       connect_args={'check_same_thread': False}, echo=True)
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

# 데이터베이스 모델 정의
Base = declarative_base()

class Member(Base):
    __tablename__ = 'members'

    mno = Column(Integer, primary_key=True, index=True)
    userid = Column(String, index=True)
    passwd = Column(String)
    name = Column(String)
    email = Column(String)
    regdate = Column(DateTime(timezone=True), server_default=func.now())

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)

# 데이터베이스 세션을 의존성으로 주입하기 위한 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic 모델
class MemberModel(BaseModel):
    mno: int
    userid: str
    name: str
    email: str
    regdate: datetime

# FastAPI 애플리케이션 생성
app = FastAPI()

@app.get('/')
def index():
    return 'Hello, SQLAlchemy and FastAPI!'

# 회원정보 조회
@app.get('/members', response_model=List[MemberModel])
def read_members(db: Session = Depends(get_db)):
    members = db.query(Member).all()
    return members

# 회원정보 추가
@app.post('/members', response_model=MemberModel)
def meadd(member: MemberModel, db: Session = Depends(get_db)):
    db_member = Member(**member.dict())
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member

# 회원정보 상세 조회
@app.get('/members/{mno}', response_model=MemberModel)
def read_member(mno: int, db: Session = Depends(get_db)):
    member = db.query(Member).filter(Member.mno == mno).first()
    return member

# 회원정보 삭제
@app.delete('/members/{mno}', response_model=MemberModel)
def delete_member(mno: int, db: Session = Depends(get_db)):
    member = db.query(Member).filter(Member.mno == mno).first()
    db.delete(member)
    db.commit()
    return member

# 회원정보 수정
@app.put('/members/{mno}', response_model=MemberModel)
def update_member(mno: int, db: Session = Depends(get_db)):
    member = db.query(Member).filter(Member.mno == mno).first()
    for key, value in dict(exclude_unset=True).items():
        setattr(member, key, value)
    db.commit()
    db.refresh(member)
    return member

if __name__ == "__main__":
    import uvicorn
    uvicorn.run('sqlalchemy02:app', reload=True)
