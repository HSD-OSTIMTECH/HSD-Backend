from app.database import create_db_and_tables
from app.routers import user_router


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.routers import example
from app.routers import announcements
from app.routers import profile
from app.routers import projects
from app.routers import achievements

app = FastAPI()

# Statik dosyaları sun
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  #T Güvenlik için sadece frontend adresi bulunmaktadır: "http://localhost:3000"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(example.router)
app.include_router(announcements.router)
app.include_router(profile.router)
app.include_router(projects.router)
app.include_router(achievements.router)
app.include_router(user_router.router)


@app.get("/")
def root():
    return {"message": "API çalışıyor"}

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
