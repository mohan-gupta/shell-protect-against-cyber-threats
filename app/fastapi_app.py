from pydantic import BaseModel

from fastapi import FastAPI

from predict import get_span

app = FastAPI()

class TextInp(BaseModel):
    text: str


app.post("/get-code")
async def get_code(inp: TextInp):
    span = get_span(text=inp.text)
    
    return {
        "response": span
    }