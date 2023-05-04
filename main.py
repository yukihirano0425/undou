from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
import os
from boto.s3.connection import S3Connection

openai.api_key = S3Connection(os.environ["openai_api_key"])

class Predict(BaseModel):
    language: str
    script: str
    error: str
    purpose: str
    

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def Hello():
    return {"Hello":"World!"}


@app.post("/")
def Hello(data: Predict):
    question_format = f"{data.language}について質問したい。\n" \
        f"以下のスクリプトを実行すると、次のようなエラーが出た。\n" \
        f"エラーの原因と解消法と、その解消に使った技術に関して詳細に解説してほしい。" \
        f"また、回答フォーマットも指定する\n\n" \
        f"・スクリプト\n" \
        f"{data.script}\n" \
        f"・エラー内容\n" \
        f"{data.error}\n\n" \
        f"・回答フォーマット\n" \
        f"1. エラー原因\n\n" \
        f"2. エラーが解消されたスクリプト\n\n" \
        f"3. エラー解消に用いた技術とその解説"
        
        
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": question_format},
        ],
    )
    return {"res": response.choices[0]["message"]["content"].strip()}
