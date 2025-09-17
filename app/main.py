from app.database import create_db_and_tables
from app.routers import user_router


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from app.routers import example
from app.routers import announcements
from app.routers import profile
from app.routers import projects
from app.routers import achievements
from app.routers import forms
from app.routers import ideas

app = FastAPI()

# Statik dosyaları sun (klasör varsa)
static_dir = "app/static"
if os.path.isdir(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

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
app.include_router(forms.router)
app.include_router(ideas.router)


@app.get("/")
def root():
    return {"message": "API çalışıyor"}

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
