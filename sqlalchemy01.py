from typing import List

from fastapi import FastAPI, Depends
from pydantic import BaseModel
from requests import Session
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker, declarative_base

# sqlalchemy
# 파이썬용 ORM 라이브러리
# https://sqlalchemy.org/


# 데이터베이스 설정
sqlite_url = 'sqlite:///python.db'
engine = create_engine(sqlite_url,
        connect_args={'check_same_thread': False}, echo=True)
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

# 데이터베이스 모델 정의
Base = declarative_base()

class Sungjuk(Base):
    __tablename__ = 'sungjuk'

    sjno = Column(Integer, primary_key=True, index=True)  # 수정된 부분
    name = Column(String, index=True)
    kor = Column(Integer)
    eng = Column(Integer)
    mat = Column(Integer)

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)


# 데이터베이스 세션을 의존성으로 주입하기 위한 함수
def get_db():
    db = SessionLocal() # 데이터베이스 세션 객체 생성
    try:
        yield db   # 파이썬 제너레이터 객체
                   # 함수가 호출될 때 비로소 객체를 반환(넘김)
    finally:
        db.close() # 데이터베이션 세션 닫음 (디비 연결 해체, 리소스 반환)


class SungjukResponse(BaseModel):
    sjno: int
    name: str
    kor: int
    eng: int
    mat: int

# FastAPI 애플리케이션 생성
app = FastAPI()

# 성적 조회
# Depends : 의존성 주입 - 디비 세션 제공
# => 코드 재사용성 향상, 관리 용이성 형성
@app.get('/sj', response_model=List[SungjukResponse])
def read_sj(db: Session = Depends(get_db)):
    sungjuks = db.query(Sungjuk).all()
    return sungjuks

# __name__: 실행중인 모듈 이름을 의미하는 매직키워드
# 만일, 파일을 직접 실행하면 __name__의 이름은 __main__으로 자동지정

if __name__ == "__main__":
    import uvicorn
    uvicorn.run('sqlalchemy01:app', reload=True)

app = FastAPI()
