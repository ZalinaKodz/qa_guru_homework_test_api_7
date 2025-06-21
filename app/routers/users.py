from fastapi import APIRouter, HTTPException, status
from fastapi_pagination import Page, paginate
from app.database import users as user_crud
from app.models.User import UserCreate, UserUpdate, UserResponse, User

router = APIRouter(prefix="/api/users", tags=["users"])

@router.get("/", response_model=Page[UserResponse])
def get_users() -> Page[UserResponse]:
    all_users = user_crud.get_users()
    return paginate(all_users)

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int) -> UserResponse:
    user = user_crud.get_user(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserResponse.model_validate(user)

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate) -> UserResponse:
    try:
        created_user = user_crud.create_user(user)
        return created_user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.patch("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_update: UserUpdate) -> UserResponse:
    user = user_crud.update_user(user_id, user_update)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserResponse.model_validate(user)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int) -> None:
    success = user_crud.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")