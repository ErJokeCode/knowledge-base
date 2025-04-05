from fastapi import APIRouter, HTTPException


router = APIRouter(
    prefix="/question",
    tags=["question"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_questions():
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/{id}")
async def get_question():
    raise HTTPException(status_code=501, detail="Not implemented")


@router.post("/")
async def create_question():
    raise HTTPException(status_code=501, detail="Not implemented")


@router.patch("/{id}")
async def update_question():
    raise HTTPException(status_code=501, detail="Not implemented")


@router.delete("/{id}")
async def delete_question():
    raise HTTPException(status_code=501, detail="Not implemented")
