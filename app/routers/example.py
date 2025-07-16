from fastapi import APIRouter

router = APIRouter(prefix="/example", tags=["Example"])

@router.get("/")
def get_example():
    return {"data": "Bu bir örnek"} 