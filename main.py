from fastapi import FastAPI

app = FastAPI()
app.title = 'Learning FastAPI'
app.version = '0.0.1'

@app.get('/', tags=['home'])
def message():
    return "Holis como andas, esto lo hice desde python"