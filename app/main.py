from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import example
from app.routers import announcements
from app.routers import profile
from app.routers import projects
from app.routers import achievements

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Güvenlik için sadece frontend adresini de yazabilirsin: ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(example.router)
app.include_router(announcements.router)
app.include_router(profile.router)
app.include_router(projects.router)
app.include_router(achievements.router)

@app.get("/")
def root():
    return {"message": "API çalışıyor"}
