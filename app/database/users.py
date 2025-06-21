from typing import Iterable, Optional
from sqlmodel import Session, select

from app.database.engine import engine
from app.models.User import User, UserCreate, UserUpdate, UserResponse

def get_user(user_id: int) -> Optional[User]:
    with Session(engine) as session:
        return session.get(User, user_id)

def get_users() -> Iterable[User]:
    with Session(engine) as session:
        return session.exec(select(User)).all()

def create_user(user_create: UserCreate) -> UserResponse:
    with Session(engine) as session:
        db_user = User(email=user_create.email, first_name=user_create.first_name,
                      last_name=user_create.last_name, avatar=user_create.avatar)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return UserResponse.model_validate(db_user)

def update_user(user_id: int, user_update: UserUpdate) -> Optional[UserResponse]:
    with Session(engine) as session:
        db_user = session.get(User, user_id)
        if not db_user:
            return None
        if user_update.email:
            db_user.email = user_update.email
        if user_update.first_name:
            db_user.first_name = user_update.first_name
        if user_update.last_name:
            db_user.last_name = user_update.last_name
        if user_update.avatar:
            db_user.avatar = user_update.avatar
        session.commit()
        session.refresh(db_user)
        return UserResponse.model_validate(db_user)

def delete_user(user_id: int) -> bool:
    with Session(engine) as session:
        db_user = session.get(User, user_id)
        if not db_user:
            return False
        session.delete(db_user)
        session.commit()
        return True