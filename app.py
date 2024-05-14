from fastapi import FastAPI
from models.settings import API_URL, API_PORT
from models.data import read_json
import uvicorn

app = FastAPI()
startup = False


@app.get("/")
def read_root():
    return {"Status": "Running"}


@app.get("/api/data/{data_id}/")
async def read_data(data_id):
    data = read_json(data_id)
    return {"data": data}


@app.get("/api/data/{data_id}/{service}")
async def read_data(data_id, service):
    data = read_json(file=f'{service}/{data_id}')

    if type(data) is str:
        return {"data": data}

    if service == 'health':
        data = {
            'temp': data['temp'],
            'voltage': data['voltage']
        }

    elif service in ['rms2', 'rmms']:
        data = {
            'x': data['x'],
            'y': data['y'],
            'z': data['z']
        }

    elif service == 'tilt':
        data = {
            'pitch': data['pitch'],
            'roll': data['roll']
        }

    elif service == 'ntc' and data['channel'] != 'ab':
        data = data[data['channel']]

    elif service == 'ntc' and data['channel'] == 'ab':
        data = {
            'a': data['a'],
            'b': data['b']
        }

    return {"data": data}


if __name__ == "__main__":
    try:
        uvicorn.run('app:app', host=API_URL, port=API_PORT, reload=True)
    except KeyboardInterrupt:
        print('Exiting...')
        exit(3)
