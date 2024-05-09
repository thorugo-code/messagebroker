from fastapi import FastAPI
from models.settings import API_URL, API_PORT
from models.data import read_json
import uvicorn

app = FastAPI()
startup = False


@app.get("/")
def read_root():
    return {"Status": "Running"}


@app.get("/api/data/{data_id}")
async def read_data(data_id):
    data = read_json(data_id)
    return {"data": data}


if __name__ == "__main__":
    uvicorn.run('app:app', host=API_URL, port=API_PORT, reload=True)
