from fastapi import FastAPI
from app.database import Base, engine
from app import  boards, columns, cards
from app.auth import router as auth_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables
Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(boards.router)
app.include_router(columns.router)
app.include_router(cards.router)

@app.get("/")
def read_root():
    return {"message": "Hello, PostgreSQL is connected!"}
