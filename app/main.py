from fastapi import FastAPI

app = FastAPI(title="modamar", description="P2P classifieds marketplace API for the Nigerian market")

@app.get("/")
def read_root():
    return {"Hello": "World"}
