from datetime import datetime
from typing import List, Optional

from fastapi import FastAPI
from fastapi.params import Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String, Integer, Sequence, DateTime, func
from sqlalchemy.orm import sessionmaker, declarative_base, Session

from sqlalchemy01 import SessionLocal

# 회원정보를 이용한 SQL CRUD
# mno, userid, passwd, name, email, regdate

sqlite_url = 'sqlite:///python.db'
engine = create_engine(sqlite_url, connect_args={}, echo=True)
SessionLocal = sessionmaker(autocommit=False,
                            autoflush=False, bind=engine)

Base = declarative_base()

class Member(Base):
    __tablename__ = 'member'

    mno = Column(Integer, Sequence('seq_member'),
                 primary_key=True, index=True)
    userid = Column(String, index=True)
    passwd = Column(String)
    name = Column(String)
    email = Column(String)
    regdate = Column(DateTime(timezone=True),
                     server_default=func.now())

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class NewMemberModel(BaseModel):
    userid: str
    passwd: str
    name: str
    email: str

class MemberModel(NewMemberModel):
    mno: int
    regdate: datetime


app = FastAPI()

@app.get('/')
def index():
    return 'Hello, sqlalchemy!!, again'


@app.get('/member', response_model=List[MemberModel])
def read_member(db: Session = Depends(get_db)):
    members = db.query(Member).all()
    return members


# @app.post('/member', response_model=NewMemberModel)
@app.post('/member', response_model=str)
def add_member(m: NewMemberModel, db: Session = Depends(get_db)):
    m = Member(**dict(m))
    db.add(m)
    db.commit()
    db.refresh(m)
    # return m
    return '데이터 입력 성공!!'


@app.get('/member/{mno}', response_model=Optional[MemberModel])
def readone_member(mno: int, db: Session = Depends(get_db)):
    member = db.query(Member).filter(Member.mno == mno).first()
    return member


@app.delete('/member/{mno}', response_model=Optional[MemberModel])
def delete_member(mno: int, db: Session = Depends(get_db)):
    member = db.query(Member).filter(Member.mno == mno).first()
    if member:
        db.delete(member)
        db.commit()
    return member


@app.put('/member/{mno}', response_model=Optional[MemberModel])
def update_member(m: MemberModel, db: Session = Depends(get_db)):
    member = db.query(Member).filter(Member.mno == m.mno).first()
    if member:
        for k, v in m.dict().items():
            setattr(member, k, v)
        db.commit()
        db.refresh(member)
    return member


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('sqlalchemy02:app', reload=True)
