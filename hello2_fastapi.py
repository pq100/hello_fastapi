from fastapi import FastAPI


# fastapi 앱 실행 방법
# python -m uvicorn 파일명 : app --reload
# python -m uvicorn hello_fastapi:app --reload

app = FastAPI()

@app.get('/')
def index():
    return 'Hello, World!!, again!!'

if __name__ == "__main__":
    import uvicorn
    uvicorn.run('hello2_fastapi:app', reload=True)

