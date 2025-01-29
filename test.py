from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def start_cmd():
    return {'Hello': 3}
