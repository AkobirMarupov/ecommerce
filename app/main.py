from fastapi import FastAPI

app = FastAPI()


@app.get('/')
async def get_root():
    return {"Asosiy qism Modeli va Kategotiyasi"}