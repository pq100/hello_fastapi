# 데이터베이스 세션을 의존성으로 주입하기 위한 함수
from datetime import datetime

from pydantic import BaseModel

# pydnatic 모델
class NewSungjukModel(BaseModel):
    sjno: int
    name: str
    kor: int
    eng: int
    mat: int

class SungjukModel(NewSungjukModel):
    sjno: int
    regdate: datetime