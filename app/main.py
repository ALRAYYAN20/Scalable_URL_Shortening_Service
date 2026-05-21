from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from .database import engine
from . import models
from . routers import auth, urls
models.Base.metadata.create_all(bind=engine)
#This tells SQLAlchemy to look at all your models and create the actual tables in PostgreSQL automatically when the app starts.

app = FastAPI()

app.include_router(auth.router)
app.include_router(urls.router)

# @app.get('/')
# def root():
#     return {'message': 'Expense Tracker API'}

@app.get("/")
def home():
    return RedirectResponse(url="/docs")