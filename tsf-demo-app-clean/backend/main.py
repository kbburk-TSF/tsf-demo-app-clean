from fastapi import FastAPI

app = FastAPI(title='TSF Demo Engine')

@app.get('/')
def root():
    return {'message': 'TSF Demo Engine API running'}
