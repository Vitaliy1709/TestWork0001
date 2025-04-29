from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.user import UserCreate, UserResponse
from app.schemas.token import Token
from app.core.security import verify_password, create_access_token, create_refresh_token, verify_refresh_token
from app.crud.crud_user import crud_user

router = APIRouter()
bearer_scheme = HTTPBearer()


@router.post(
    "/register",
    response_model=UserResponse,
    summary="Register a new user",
)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    user = await crud_user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = await crud_user.create(db, user_in=user_in)
    return user


@router.post(
    "/login",
    response_model=Token,
    summary="User authentication and issuance of a pair of JWT tokens (access + refresh).",
)
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: AsyncSession = Depends(get_db),
):
    user = await crud_user.get_by_email(db, email=form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    if not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})

    return Token(
        access_token=access_token,
        refresh_token=refresh_token
    )


@router.post(
    "/refresh",
    response_model=Token,
    summary="Updating the access token using a refresh token.",
)
async def refresh_token(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    refresh_token = credentials.credentials

    # Checking the refresh token
    user_id = verify_refresh_token(refresh_token)

    # Create a new access token and a new refresh token
    access_token = create_access_token(data={"sub": str(user_id)})
    new_refresh_token = create_refresh_token(data={"sub": str(user_id)})

    return Token(access_token=access_token, refresh_token=new_refresh_token)
