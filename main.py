from fastapi import FastAPI
from indb import generate_product

app =FastAPI()

products = generate_product()

@app.get('/')
def get_producst():
    return{"succes":products}

